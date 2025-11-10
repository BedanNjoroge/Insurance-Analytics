# Insurance-Analytics

**Project Overview**

This project explores how demographic and health-related factors such as age, BMI, smoking status, and number of dependants  influence insurance charges.

It combines data analysis, machine learning, and dashboard design to deliver both predictive insights and interactive data visualizations for better decision-making in the insurance industry.

**Objectives**
1. Identify key factors influencing insurance charges.
2. Discover target market segments (e.g., by age or BMI bracket).
3. Build a machine learning model to predict insurance charges.
4. Develop interactive dashboards for data-driven decision support.

**Project Workflow**
1. Exploratory Data Analysis (EDA)
   
   Performed detailed EDA using Python to uncover relationships between variables.

2. Machine Learning

   Built ML models and deployed a Streamlit web app for predicting insurance charges using features such as: Age, BMI, Number of children, Smoker status, Gender, Region.

   Streamlit app link: https://insurance-analytics-hs.streamlit.app/

3. Dashboards & Visualization
   
   Developed 3 interactive dashboards for every kind of stakeholder;

   a. Excel + Power Query
   
   <img width="1552" height="555" alt="image" src="https://github.com/user-attachments/assets/153ea14f-dcc1-4346-b1f9-ea526ab49cae" />

   
   b. Power BI
   
   <img width="1276" height="726" alt="image" src="https://github.com/user-attachments/assets/1e93deb8-e7b2-4fed-a702-c768a876f506" />


   c. Plotly Dash

   <img width="1585" height="762" alt="image" src="https://github.com/user-attachments/assets/72b4d9fc-0630-4af1-9220-5efa632bc421" />


**Key Insights**
1. Smokers pay on average 4x more than non-smokers (your lungs aren’t the only thing taking a hit😉).
2. Ages 19–25 are the most frequent policyholders — looks like Gen Z is insuring early!
3. Obese I and Overweight individuals were the most common in taking up insurance.
4. Smoker status and Age were the strongest predictors of insurance charges.

   <img width="709" height="472" alt="image" src="https://github.com/user-attachments/assets/30250742-437a-490c-a34e-4e9ce38d5255" />


**Business Recommendations**
1. Target potential policyholders aged 19–25 with health and family plans.
2. Offer BMI-based discounts to encourage healthier lifestyles.
3. Reward non-smokers (and maybe cheer on those trying to quit💪).

```bash
Folder Structure:

Insurance-Analytics/
│
├── Data/
│   └── insurance.csv
│
├── Notebooks/
│   ├── eda.ipynb
│   ├── model.ipynb
│
├── Dashboards/
│   ├── dash_dashboard.py
│   ├── powerbi_dashboard.pbix
│   ├── excel_dashboard.xlsx
│   ├── powerbi_dashboard.pdf
│   ├── assets/
│       └── style.css
├── Streamlit_App/
│     └──app_streamlit.py
│   
├── README.md
└── requirements.txt
