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
        pregnancies = st.number_input("Pregnancies", 0.0, 20.0, 1.0)
        glucose = st.number_input("Glucose (mg/dL)", 0.0, 300.0, 100.0)
        blood_pressure = st.number_input("Blood Pressure (mmHg)", 0.0, 200.0, 72.0)
        skin_thickness = st.number_input("Skin Thickness (mm)", 0.0, 100.0, 20.0)
    with col2:
        insulin = st.number_input("Insulin (µU/mL)", 0.0, 900.0, 80.0)
        bmi = st.number_input("BMI", 0.0, 70.0, 25.0)
        dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.3)
        age = st.number_input("Age (Years)", 1, 120, 30)

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
    st.subheader("ℹ️ Feature Information")
    st.markdown("""
| Feature | Meaning |
|------|---------------------------|
| Pregnancies | Number of pregnancies |
| Glucose | Blood sugar level |
| Blood Pressure | Diastolic BP |
| Skin Thickness | Body fat thickness |
| Insulin | Insulin in blood |
| BMI | Body Mass Index |
| DPF | Family diabetes factor |
| Age | Age in years |
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
