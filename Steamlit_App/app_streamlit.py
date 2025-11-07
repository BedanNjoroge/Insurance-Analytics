#Import necessary libraries
import streamlit as st
import pandas as pd
import joblib

# -------------------------------
# 🔹 Load trained XGBoost model
# -------------------------------
xgb_model = joblib.load("xgb_insurance_model.pkl")

# -------------------------------
# 🎨 PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="Insurance Charge Predictor 💰",
    page_icon="💵",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------------------
# 🏠 SIDEBAR INFO
# -------------------------------
st.sidebar.title("ℹ️ About the App")
st.sidebar.markdown("""
This app predicts **medical insurance charges** using a trained XGBoost model.

It considers:
- Age Bracket 🧓  
- BMI Bracket ⚖️  
- Smoking Habits 🚬  
- Region 🌍  
- Number of Dependents 👨‍👩‍👧‍👦  
- Gender ⚧️  

After entering your details, click **Predict** to estimate your insurance charge.
""")

st.sidebar.info("💡 Note: The prediction is an estimate based on statistical patterns — actual charges may vary.")

# -------------------------------
# 🧾 ENCODING MAPPINGS
# -------------------------------
age_bracket_options = {
    "0-18 years": 1,
    "19-25 years": 2,
    "26-35 years": 3,
    "36-45 years": 4,
    "46-55 years": 5,
    "56-60 years": 6,
    "61+ years": 7
}

bmi_bracket_options = {
    "Underweight (<18.5)": 1,
    "Normal (18.5 - 24.9)": 2,
    "Overweight (25 - 29.9)": 3,
    "Obese (≥30)": 4
}

region_mapping = {
    "Northeast": 0,
    "Northwest": 1,
    "Southeast": 2,
    "Southwest": 3
}

# -------------------------------
# 🧮 MAIN PAGE
# -------------------------------
st.title("💰 Insurance Charge Predictor")
st.markdown("Predict medical insurance charges based on your health and lifestyle details.")

col1, col2 = st.columns(2)

with col1:
    age_choice = st.selectbox("👶 Age Range", list(age_bracket_options.keys()))
    bmi_choice = st.selectbox("⚖️ BMI Range", list(bmi_bracket_options.keys()))
    sex = st.radio("⚧️ Sex", ["Male", "Female"])

with col2:
    children = st.number_input("👨‍👩‍👧 Number of Children", 0, 5, 0)
    smoker = st.radio("🚬 Smoker?", ["Yes", "No"])
    region = st.selectbox("🌍 Region", list(region_mapping.keys()))

# -------------------------------
# 🧮 PREPARE INPUT DATA
# -------------------------------
input_data = pd.DataFrame({
    'age_bracket': [age_bracket_options[age_choice]],
    'bmi_bracket': [bmi_bracket_options[bmi_choice]],
    'sex': [1 if sex == "Male" else 0],
    'children': [children],
    'smoker': [1 if smoker == "Yes" else 0],
    'region': [region_mapping[region]]
})

# -------------------------------
# 🔍 PREDICTION
# -------------------------------
st.write("---")
if st.button("🔮 Predict Insurance Charge"):
    predicted_charge = xgb_model.predict(input_data)[0]
    st.success(f"💵 **Estimated Insurance Charge:** ${predicted_charge:,.2f}")

