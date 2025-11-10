# Import necessary libraries
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import os

# -----------------------------
# Load data
# -----------------------------
#Load the dataset
DATA_FILE = "insurance.csv"
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"{DATA_FILE} not found. Place your dataset in the app folder.")

df = pd.read_csv(DATA_FILE)

# create brackets if raw age & bmi exist
if 'age_bracket' not in df.columns and 'age' in df.columns:
    bins_age = [0, 18, 25, 30, 35, 40, 45, 50, 55, 60, 65]
    labels_age = ['0–18','19–25','26–30','31–35','36–40','41–45','46–50','51–55','56–60','61–65']
    df['age_bracket'] = pd.cut(df['age'], bins=bins_age, labels=labels_age, right=True, include_lowest=True)

if 'bmi_bracket' not in df.columns and 'bmi' in df.columns:
    bins_bmi = [0, 18.5, 24.9, 29.9, 34.9, 39.9, 100]
    labels_bmi = ['Underweight', 'Normal', 'Overweight', 'Obese I', 'Obese II', 'Obese III']
    df['bmi_bracket'] = pd.cut(df['bmi'], bins=bins_bmi, labels=labels_bmi, right=False, include_lowest=True)

df['smoker'] = df['smoker'].astype(str).str.strip().str.capitalize().replace({'Y': 'Yes', 'N': 'No'})
df['sex'] = df['sex'].astype(str).str.strip().str.capitalize()
df['region'] = df['region'].astype(str)
df['children'] = pd.to_numeric(df['children'], errors='coerce').fillna(0).astype(int)
df['charges'] = pd.to_numeric(df['charges'], errors='coerce')
df = df.dropna(subset=['age_bracket', 'bmi_bracket', 'sex', 'children', 'smoker', 'region', 'charges'])
# -----------------------------
# App init
# -----------------------------
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server
app.title = "Insurance Dashboard"

# -----------------------------
# Components
# -----------------------------
theme_toggle = dbc.Switch(id="theme-toggle", label="🌙 Dark Mode", value=False, className="theme-toggle")

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("🏠 Overview", href="/", active="exact")),
        dbc.NavItem(dbc.NavLink("📊 Age Insights", href="/age", active="exact")),
        dbc.NavItem(dbc.NavLink("⚖️ BMI Insights", href="/bmi", active="exact")),
    ],
    brand="🛡️📊 Insurance Analytics",
    brand_href="/",
    color="primary",
    dark=True,
    className="navbar",
)

# -----------------------------
# KPI helper
# -----------------------------
def create_kpi_card(icon, title, value):
    return dbc.Card(
        dbc.CardBody([
            html.Div(icon, className="kpi-icon"),
            html.Div([
                html.Div(title, className="kpi-title"),
                html.Div(value, className="kpi-value")
            ], className="kpi-text")
        ]),
        className="kpi-card"
    )

# -----------------------------
# Page layouts
# -----------------------------
def overview_page():
    avg_charge = f"${df['charges'].mean():,.0f}"
    typical_age = df['age_bracket'].mode().iloc[0]
    typical_bmi = df['bmi_bracket'].mode().iloc[0]
    avg_children = f"{df['children'].mean():.0f}"

    #print(df.groupby('age_bracket', observed=False)['charges'].mean().reset_index().to_string(index=False))

    kpis = dbc.Row([
        dbc.Col(create_kpi_card("💰", "Average Insurance Charge", avg_charge), md=3),
        dbc.Col(create_kpi_card("👥", "Core Age Bracket", typical_age), md=3),
        dbc.Col(create_kpi_card("⚖️", "Core BMI Bracket", typical_bmi), md=3),
        dbc.Col(create_kpi_card("👶", "Avg Number of Dependants", avg_children), md=3),
    ], className="kpi-row")

    fig_age = px.bar(df.groupby('age_bracket', observed=False)['charges'].mean().reset_index(),
                     x='age_bracket', y='charges', title='Average Charges by Age Bracket')
    fig_bmi = px.bar(df.groupby('bmi_bracket', observed=False)['charges'].mean().reset_index(),
                     x='bmi_bracket', y='charges', title='Average Charges by BMI Bracket')
    fig_donut = px.pie(df.groupby('smoker', observed=False)['charges'].mean().reset_index(),
                       names='smoker', values='charges', title='Average Charges by Smoker Status', hole=0.4)
    
    fig_age.update_traces(hovertemplate="Average Charge: $%{y:,.2f}<br>Age: %{label}<extra></extra>")
    fig_bmi.update_traces(hovertemplate="Average Charge: $%{y:,.2f}<br>BMI: %{label}<extra></extra>")
    fig_donut.update_traces(hovertemplate="Smoker Status: %{label}<br>Average Charge: $%{value:,.2f}<br>Share: %{percent}<extra></extra>")

    charts = dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_age), md=11.5), #was md=6
        dbc.Col(dcc.Graph(figure=fig_bmi), md=11.5),
        dbc.Col(dcc.Graph(figure=fig_donut), md=11.5),
    ], className="chart-row")

    return html.Div([kpis, charts], className="page-content")

def age_page():
    fig_gender = px.bar(df.groupby(['age_bracket', 'sex'], observed=False)['charges'].mean().reset_index(),
                        x='age_bracket', y='charges', color='sex', barmode='group',
                        title='Avg Charges by Age Bracket (Gender)')
    fig_smoker = px.bar(df.groupby(['age_bracket', 'smoker'], observed=False)['charges'].mean().reset_index(),
                        x='age_bracket', y='charges', color='smoker', barmode='group',
                        title='Avg Charges by Age Bracket (Smoker)')
    fig_children = px.bar(df.groupby(['age_bracket', 'children'], observed=False)['charges'].mean().reset_index(),
                          x='age_bracket', y='charges', color='children', barmode='group',
                          title='Avg Charges by Age Bracket (Dependants)')
    fig_region = px.bar(df.groupby(['age_bracket', 'region'], observed=False)['charges'].mean().reset_index(),
                        x='age_bracket', y='charges', color='region', barmode='group',
                        title='Avg Charges by Age Bracket (Region)')
    
    fig_gender.update_traces(
        hovertemplate="Gender: %{customdata[0]}<br>Age: %{x}<br>Average Charge: $%{y:,.2f}<extra></extra>",
        customdata=df.groupby(['age_bracket', 'sex'], observed=False)['charges'].mean().reset_index()[['sex']]
    )
    fig_smoker.update_traces(
        hovertemplate="Smoker Status: %{customdata[0]}<br>Age: %{x}<br>Average Charge: $%{y:,.2f}<extra></extra>",
        customdata=df.groupby(['age_bracket', 'smoker'], observed=False)['charges'].mean().reset_index()[['smoker']]
    )
    fig_children.update_traces(
        hovertemplate="No of Dependants: %{customdata[0]}<br>Age: %{x}<br>Average Charge: $%{y:,.2f}<extra></extra>",
        customdata=df.groupby(['age_bracket', 'children'], observed=False)['charges'].mean().reset_index()[['children']]
    )
    fig_region.update_traces(
        hovertemplate="Region: %{customdata[0]}<br>Age: %{x}<br>Average Charge: $%{y:,.2f}<extra></extra>",
        customdata=df.groupby(['age_bracket', 'region'], observed=False)['charges'].mean().reset_index()[['region']]
    )

    return html.Div([
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_gender), md=6), dbc.Col(dcc.Graph(figure=fig_smoker), md=6)]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_children), md=6), dbc.Col(dcc.Graph(figure=fig_region), md=6)]),
    ], className="page-content")

def bmi_page():
    fig_gender = px.bar(df.groupby(['bmi_bracket', 'sex'], observed=False)['charges'].mean().reset_index(),
                        x='bmi_bracket', y='charges', color='sex', barmode='group',
                        title='Avg Charges by BMI Bracket (Gender)')
    fig_smoker = px.bar(df.groupby(['bmi_bracket', 'smoker'], observed=False)['charges'].mean().reset_index(),
                        x='bmi_bracket', y='charges', color='smoker', barmode='group',
                        title='Avg Charges by BMI Bracket (Smoker)')
    fig_children = px.bar(df.groupby(['bmi_bracket', 'children'], observed=False)['charges'].mean().reset_index(),
                          x='bmi_bracket', y='charges', color='children', barmode='group',
                          title='Avg Charges by BMI Bracket (Dependants)')
    fig_region = px.bar(df.groupby(['bmi_bracket', 'region'], observed=False)['charges'].mean().reset_index(),
                        x='bmi_bracket', y='charges', color='region', barmode='group',
                        title='Avg Charges by BMI Bracket (Region)')
    
    fig_gender.update_traces(
        hovertemplate="Gender: %{customdata[0]}<br>BMI: %{x}<br>Average Charge: $%{y:,.2f}<extra></extra>",
        customdata=df.groupby(['bmi_bracket', 'sex'], observed=False)['charges'].mean().reset_index()[['sex']]
    )
    fig_smoker.update_traces(
        hovertemplate="Smoker Status: %{customdata[0]}<br>BMI: %{x}<br>Average Charge: $%{y:,.2f}<extra></extra>",
        customdata=df.groupby(['bmi_bracket', 'smoker'], observed=False)['charges'].mean().reset_index()[['smoker']]
    )
    fig_children.update_traces(
        hovertemplate="No of Dependants: %{customdata[0]}<br>BMI: %{x}<br>Average Charge: $%{y:,.2f}<extra></extra>",
        customdata=df.groupby(['bmi_bracket', 'children'], observed=False)['charges'].mean().reset_index()[['children']]
    )
    fig_region.update_traces(
        hovertemplate="Region: %{customdata[0]}<br>BMI Bracket: %{x}<br>Average Charge: $%{y:,.2f}<extra></extra>",
        customdata=df.groupby(['bmi_bracket', 'region'], observed=False)['charges'].mean().reset_index()[['region']]
    )

    return html.Div([
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_gender), md=6), dbc.Col(dcc.Graph(figure=fig_smoker), md=6)]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_children), md=6), dbc.Col(dcc.Graph(figure=fig_region), md=6)]),
    ], className="page-content")

# -----------------------------
# Layout
# -----------------------------
app.layout = html.Div(
    id="root",
    children=[
        navbar,
        html.Div(className="toggle-row", children=[theme_toggle]),
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content", className="page-wrapper"),
    ],
)

# -----------------------------
# Callbacks (no dcc.Store)
# -----------------------------
@app.callback(
    Output("root", "className"),
    Input("theme-toggle", "value")
)
def toggle_theme(is_dark):
    return "app-root dark-theme" if is_dark else "app-root light-theme"

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/age":
        return age_page()
    elif pathname == "/bmi":
        return bmi_page()
    return overview_page()

# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=8051)