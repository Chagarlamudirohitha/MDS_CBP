import streamlit as st
import numpy as np
import joblib
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from streamlit_option_menu import option_menu

# Load model and scaler
scaler = joblib.load("scaler.joblib")
model = joblib.load("model_rf.joblib")

# PDF generator function (NO FILE SAVING)
def generate_pdf(name, prediction, values_dict):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(140, 800, "Diabetes Report Summary")

    # Patient info
    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Patient Name: {name}")
    c.drawString(50, 740, f"Risk Status: {'Likely Diabetic' if prediction == 1 else 'Not Diabetic'}")

    # Values
    c.drawString(50, 710, "Health Inputs:")
    y = 690
    for k, v in values_dict.items():
        c.drawString(60, y, f"{k}: {v}")
        y -= 20

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# Page config
st.set_page_config(page_title="Diabetes Risk Assistant", page_icon="🩺", layout="centered")

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Predict", "Info", "Tips"],
        icons=["activity", "info-circle", "heart"],
        default_index=0
    )

st.title("🩺 Diabetes Prediction Assistant")
st.write("AI-powered health screening tool using Machine Learning.")

# -------------------- Prediction Page --------------------
if selected == "Predict":
    st.subheader("🧍 Patient Details")
    name = st.text_input("👤 Patient Name", placeholder="Enter Patient Name")

    col1, col2 = st.columns(2)
    with col1:
        pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1, step=1)
        glucose = st.number_input("Glucose (mg/dL)", min_value=0.0, max_value=300.0, value=100.0, step=1.0)
        blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=0.0, max_value=200.0, value=72.0, step=1.0)
        skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0.0, max_value=100.0, value=20.0, step=1.0)
    with col2:
        insulin = st.number_input("Insulin (µU/mL)", min_value=0.0, max_value=900.0, value=80.0, step=1.0)
        bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=25.0, step=0.1)
        dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.3, step=0.01)
        age = st.number_input("Age (Years)", min_value=1, max_value=120, value=30, step=1)

    if st.button("🔍 Predict"):
        input_data = scaler.transform([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
        prediction = model.predict(input_data)[0]

        # Normal/healthy values
        normal_values = {"Glucose": 120, "Blood Pressure": 80, "BMI": 24, "Insulin": 120}
        user_values = {"Glucose": glucose, "Blood Pressure": blood_pressure, "BMI": bmi, "Insulin": insulin}

        # Chart
        st.subheader("📊 Health Metrics Comparison")
        chart_data = {
            "Metric": list(user_values.keys()),
            "Your Value": list(user_values.values()),
            "Healthy Value": list(normal_values.values())
        }
        st.bar_chart(chart_data)

        # Result message
        if prediction == 1:
            st.error(f"🚨 **{name} is likely Diabetic**")
            st.info("""
### 🩺 AI-Recommended Tips
- 🍎 Eat fruits & vegetables
- 🚶‍♂️ Walk 30–45 mins daily
- ❌ Avoid sugar & junk food
- 💧 Stay hydrated
- 🛌 Sleep 7–8 hours
- 🔁 Regular check-ups
""")
        else:
            st.success(f"✅ **{name} is Not Diabetic**")
            st.info("""
### ✅ Stay Healthy
- Balanced diet 🥗  
- Regular exercise 💪  
- Drink water 💧  
- Reduce sugar 🍬  
""")

        # PDF buffer
        pdf_buffer = generate_pdf(name, prediction, user_values)

        # Download button
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_buffer,
            file_name="diabetes_report.pdf",
            mime="application/pdf"
        )

# -------------------- Info Page --------------------
if selected == "Info":
    st.subheader("ℹ️ Feature Information & Ranges")
    
    st.markdown("""
    ### 🤰 **Pregnancies** (Integer)
    - **What it means:** Total number of times you've been pregnant
    - **Typical Range:** 0-15 pregnancies (most women have 0-5)
    - **Note:** Higher pregnancies can increase diabetes risk due to gestational diabetes history
    
    ---
    
    ### 🩸 **Glucose** (mg/dL)
    - **What it means:** Amount of sugar in your blood (plasma glucose concentration)
    - **Normal (Fasting):** 70-99 mg/dL
    - **Pre-diabetic:** 100-125 mg/dL
    - **Diabetic:** 126+ mg/dL
    - **After eating:** Can go up to 140-180 mg/dL normally
    - **Note:** This is the most important diabetes indicator
    
    ---
    
    ### 💓 **Blood Pressure** (mmHg)
    - **What it means:** Diastolic blood pressure (the lower number in BP reading like 120/80)
    - **Normal:** 60-80 mmHg
    - **Elevated:** 80-89 mmHg
    - **High:** 90+ mmHg
    - **Note:** People with diabetes often have high blood pressure too
    
    ---
    
    ### 📏 **Skin Thickness** (mm)
    - **What it means:** Triceps skin fold thickness, which measures body fat percentage
    - **Typical Range:** 10-50 mm
    - **Average for women:** 20-30 mm
    - **Note:** Used to estimate body fat, higher values suggest obesity
    
    ---
    
    ### 💉 **Insulin** (µU/mL)
    - **What it means:** Serum insulin level - the hormone that controls blood sugar
    - **Normal (Fasting):** 2.6-24.9 µU/mL
    - **Normal (After eating):** 16-166 µU/mL
    - **Note:** Diabetics may have very high or very low insulin levels
    
    ---
    
    ### ⚖️ **BMI (Body Mass Index)**
    - **What it means:** Body Mass Index - your weight relative to your height
    - **Formula:** Weight (kg) ÷ [Height (m)]²
    - **Underweight:** Below 18.5
    - **Normal weight:** 18.5-24.9
    - **Overweight:** 25.0-29.9
    - **Obese:** 30.0-39.9
    - **Severely obese:** 40+
    - **Note:** Higher BMI greatly increases diabetes risk
    
    ---
    
    ### 🧬 **Diabetes Pedigree Function (DPF)**
    - **What it means:** A score showing your genetic risk based on family diabetes history
    - **Typical Range:** 0.08-2.5
    - **Low risk:** 0.08-0.5 (little family history)
    - **Medium risk:** 0.5-1.0
    - **High risk:** 1.0+ (strong family history)
    - **Note:** Calculated from age of relatives when diagnosed and relationship to you
    
    ---
    
    ### 👶👴 **Age** (Years)
    - **What it means:** Your current age
    - **Common Range:** 1-120 years
    - **Higher Risk:** Age 45 and above
    - **Note:** Risk of Type 2 diabetes increases significantly after age 45
    """)

# -------------------- Tips Page --------------------
if selected == "Tips":
    st.subheader("❤️ Daily Health Tips")
    st.write("""
✅ Walk daily  
✅ Eat high-fiber foods  
✅ Drink 3–4L water  
✅ Avoid smoking & alcohol  
✅ Cut sugar  
✅ Sleep 7–8 hours  
""")

st.write("---")
st.caption("Made with ❤️ using Streamlit & Machine Learning")