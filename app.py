import streamlit as st
import numpy as np
import joblib
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from streamlit_option_menu import option_menu

# Load model and scaler
scaler = joblib.load("scaler.joblib")
model = joblib.load("model_rf.joblib")

# Enhanced PDF generator function
def generate_pdf(name, prediction, input_values, all_inputs):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Header with background
    c.setFillColorRGB(0.2, 0.4, 0.8)
    c.rect(0, 750, width, 92, fill=True, stroke=False)
    
    # Title
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(120, 800, "Diabetes Risk Assessment Report")
    c.setFont("Helvetica", 10)
    c.drawString(240, 780, "AI-Powered Health Analysis")
    
    # Patient Info Box
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 720, f"Patient: {name}")
    c.setFont("Helvetica", 11)
    c.drawString(50, 700, f"Date: November 09, 2025")
    
    # Risk Status Box
    y_pos = 660
    if prediction == 1:
        c.setFillColorRGB(0.8, 0.2, 0.2)
        c.rect(50, y_pos-5, 200, 30, fill=True, stroke=False)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(70, y_pos+5, "⚠ HIGH RISK - Likely Diabetic")
    else:
        c.setFillColorRGB(0.2, 0.7, 0.3)
        c.rect(50, y_pos-5, 200, 30, fill=True, stroke=False)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(80, y_pos+5, "✓ LOW RISK - Not Diabetic")
    
    # Health Metrics Section
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, 610, "Health Metrics Analysis:")
    
    c.setFont("Helvetica", 10)
    y = 585
    
    # Define normal ranges
    metrics = {
        "Pregnancies": (all_inputs[0], "0-5 typical", int(all_inputs[0]) <= 5),
        "Glucose": (all_inputs[1], "70-99 mg/dL normal", 70 <= all_inputs[1] < 100),
        "Blood Pressure": (all_inputs[2], "60-80 mmHg normal", 60 <= all_inputs[2] <= 80),
        "Skin Thickness": (all_inputs[3], "20-30 mm average", 20 <= all_inputs[3] <= 30),
        "Insulin": (all_inputs[4], "2.6-25 µU/mL fasting", 2.6 <= all_inputs[4] <= 25),
        "BMI": (all_inputs[5], "18.5-24.9 normal", 18.5 <= all_inputs[5] < 25),
        "Diabetes Pedigree": (all_inputs[6], "< 0.5 low risk", all_inputs[6] < 0.5),
        "Age": (all_inputs[7], "< 45 lower risk", int(all_inputs[7]) < 45)
    }
    
    for metric, (value, normal_range, is_normal) in metrics.items():
        # Metric name
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, y, f"{metric}:")
        
        # Value
        c.setFont("Helvetica", 10)
        c.drawString(200, y, f"{value:.2f}" if isinstance(value, float) and metric not in ["Pregnancies", "Age"] else f"{int(value)}")
        
        # Normal range
        c.setFillColorRGB(0.4, 0.4, 0.4)
        c.drawString(280, y, f"(Normal: {normal_range})")
        
        # Status indicator
        if is_normal:
            c.setFillColorRGB(0.2, 0.7, 0.3)
            c.drawString(480, y, "✓")
        else:
            c.setFillColorRGB(0.8, 0.2, 0.2)
            c.drawString(480, y, "⚠")
        
        c.setFillColorRGB(0, 0, 0)
        y -= 25
    
    # Recommendations Section
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y-10, "Recommendations:")
    y -= 30
    
    c.setFont("Helvetica", 10)
    if prediction == 1:
        recommendations = [
            "• Consult a healthcare provider immediately for proper diagnosis",
            "• Monitor blood glucose levels regularly",
            "• Follow a balanced, low-sugar diet rich in vegetables",
            "• Exercise for at least 30-45 minutes daily (walking, cycling)",
            "• Maintain a healthy weight (target BMI: 18.5-24.9)",
            "• Stay hydrated - drink 8-10 glasses of water daily",
            "• Get 7-8 hours of quality sleep each night",
            "• Avoid processed foods, sugary drinks, and excessive carbs",
            "• Schedule regular check-ups and blood tests"
        ]
    else:
        recommendations = [
            "• Continue maintaining a healthy lifestyle",
            "• Eat a balanced diet with fruits, vegetables, and whole grains",
            "• Exercise regularly - at least 150 minutes per week",
            "• Keep your weight in the healthy BMI range",
            "• Limit sugar and processed food intake",
            "• Stay hydrated throughout the day",
            "• Get annual health check-ups",
            "• Monitor any family history of diabetes"
        ]
    
    for rec in recommendations:
        c.drawString(60, y, rec)
        y -= 18
        if y < 80:  # Start new page if needed
            c.showPage()
            y = 800
    
    # Footer
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, 50, "Disclaimer: This is an AI-based screening tool and NOT a medical diagnosis.")
    c.drawString(50, 38, "Please consult a qualified healthcare professional for proper medical advice and treatment.")
    
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
        options=["Predict", "Calculators", "Info", "Tips"],
        icons=["activity", "calculator", "info-circle", "heart"],
        default_index=0
    )

st.title("🩺 Diabetes Prediction Assistant")
st.write("AI-powered health screening tool using Machine Learning.")

# -------------------- Prediction Page --------------------
if selected == "Predict":
    st.subheader("🧍 Patient Details")
    name = st.text_input("👤 Patient Name", placeholder="Enter Patient Name")
    
    st.info("💡 **Don't know your BMI or other values?** Use the **Calculators** page from the sidebar!")

    col1, col2 = st.columns(2)
    with col1:
        pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1, step=1, help="Number of times pregnant")
        glucose = st.number_input("Glucose (mg/dL)", min_value=0.0, max_value=300.0, value=100.0, step=1.0, help="Blood sugar level - can be measured at home or clinic")
        blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=0.0, max_value=200.0, value=72.0, step=1.0, help="Diastolic BP - the lower number in your BP reading")
        skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0.0, max_value=100.0, value=20.0, step=1.0, help="Can be measured with calipers or estimated as 20-30 for average")
    with col2:
        insulin = st.number_input("Insulin (µU/mL)", min_value=0.0, max_value=900.0, value=80.0, step=1.0, help="Requires blood test - use average 80 if unknown")
        bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=25.0, step=0.1, help="Use BMI calculator in Calculators page")
        dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.3, step=0.01, help="Use DPF calculator if you have family history")
        age = st.number_input("Age (Years)", min_value=1, max_value=120, value=30, step=1)

    if st.button("🔍 Predict"):
        if not name:
            st.warning("Please enter patient name")
        else:
            input_data = scaler.transform([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
            prediction = model.predict(input_data)[0]

            # Normal/healthy values
            normal_values = {"Glucose": 85, "Blood Pressure": 75, "BMI": 22, "Insulin": 80}
            user_values = {"Glucose": glucose, "Blood Pressure": blood_pressure, "BMI": bmi, "Insulin": insulin}

            # Chart
            st.subheader("📊 Health Metrics Comparison")
            chart_data = {
                "Metric": list(user_values.keys()),
                "Your Value": list(user_values.values()),
                "Optimal Value": list(normal_values.values())
            }
            st.bar_chart(chart_data)

            # Result message
            if prediction == 1:
                st.error(f"🚨 **{name} is at HIGH RISK for Diabetes**")
                st.warning("⚠️ This is a screening tool, NOT a diagnosis. Please consult a doctor immediately.")
                st.info("""
### 🩺 Immediate Action Steps
- 📞 **Schedule a doctor's appointment** for proper diagnosis
- 🩸 **Get a blood test** (HbA1c and fasting glucose)
- 🍎 **Start eating healthy** - more vegetables, less sugar
- 🚶‍♂️ **Walk 30-45 minutes daily**
- 💧 **Drink 8-10 glasses of water** daily
- ❌ **Avoid sugar, junk food, and sodas**
- 🛌 **Get 7-8 hours of sleep**
- 📝 **Monitor your blood sugar** regularly
""")
            else:
                st.success(f"✅ **{name} is at LOW RISK for Diabetes**")
                st.info("""
### ✅ Keep Up the Good Work!
- 🥗 Continue balanced diet  
- 💪 Regular exercise (150 min/week)  
- 💧 Stay hydrated  
- 🍬 Limit sugar intake  
- 📅 Annual health check-ups
""")

            # PDF buffer with all inputs
            all_inputs = [pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]
            pdf_buffer = generate_pdf(name, prediction, user_values, all_inputs)

            # Download button
            st.download_button(
                label="📄 Download Detailed PDF Report",
                data=pdf_buffer,
                file_name=f"{name.replace(' ', '_')}_diabetes_report.pdf",
                mime="application/pdf"
            )

# -------------------- Calculators Page --------------------
if selected == "Calculators":
    st.subheader("🧮 Health Calculators")
    
    # BMI Calculator
    st.markdown("### ⚖️ BMI Calculator")
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.1)
    with col2:
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.1)
    
    if st.button("Calculate BMI"):
        height_m = height / 100
        bmi_result = weight / (height_m ** 2)
        st.success(f"**Your BMI: {bmi_result:.1f}**")
        
        if bmi_result < 18.5:
            st.info("📊 Category: **Underweight**")
        elif 18.5 <= bmi_result < 25:
            st.success("📊 Category: **Normal Weight** ✓")
        elif 25 <= bmi_result < 30:
            st.warning("📊 Category: **Overweight**")
        else:
            st.error("📊 Category: **Obese**")
        
        st.write(f"💡 Use **{bmi_result:.1f}** in the Predict page")
    
    st.divider()
    
    # DPF Calculator
    st.markdown("### 🧬 Diabetes Pedigree Function (DPF) Estimator")
    st.write("This estimates your genetic risk based on family history")
    
    parents_diabetes = st.radio("Do your parents have diabetes?", ["No", "One parent", "Both parents"])
    siblings_diabetes = st.number_input("Number of siblings with diabetes", min_value=0, max_value=10, value=0, step=1)
    grandparents_diabetes = st.radio("Do your grandparents have diabetes?", ["No", "One", "Two or more"])
    
    if st.button("Calculate DPF"):
        # Simple DPF estimation formula
        dpf_score = 0.08  # Base value
        
        if parents_diabetes == "One parent":
            dpf_score += 0.4
        elif parents_diabetes == "Both parents":
            dpf_score += 0.8
        
        dpf_score += siblings_diabetes * 0.15
        
        if grandparents_diabetes == "One":
            dpf_score += 0.1
        elif grandparents_diabetes == "Two or more":
            dpf_score += 0.2
        
        dpf_score = min(dpf_score, 2.5)  # Cap at 2.5
        
        st.success(f"**Your estimated DPF: {dpf_score:.2f}**")
        
        if dpf_score < 0.5:
            st.success("📊 Risk Level: **Low genetic risk** ✓")
        elif dpf_score < 1.0:
            st.warning("📊 Risk Level: **Medium genetic risk**")
        else:
            st.error("📊 Risk Level: **High genetic risk** - Extra caution needed")
        
        st.write(f"💡 Use **{dpf_score:.2f}** in the Predict page")
    
    st.divider()
    
    # Blood Pressure Guide
    st.markdown("### 💓 Blood Pressure Guide")
    st.write("""
    **How to measure at home:**
    1. Sit quietly for 5 minutes before measuring
    2. Use a digital BP monitor (available at pharmacies)
    3. Take reading on your upper arm
    4. The **second number (diastolic)** is what you need
    5. Example: If reading is 120/80, use **80**
    
    **Don't have a BP monitor?** 
    - Use **72-80** as a typical healthy value
    - Get it measured at a pharmacy or clinic
    """)
    
    st.divider()
    
    # Other estimates
    st.markdown("### 📏 Quick Estimates")
    st.write("""
    **Skin Thickness:** 
    - If you don't have calipers, use **20-25 mm** for average build
    - Use **30-40 mm** if overweight
    - Use **15-20 mm** if slim
    
    **Insulin:** 
    - Requires blood test at a lab
    - If unknown, use **80 µU/mL** as average fasting value
    - Or leave it at default until you get tested
    
    **Glucose:**
    - Can be measured at home with a glucometer (~₹500-1000)
    - Or get tested at any diagnostic lab
    - Fasting glucose test is most common
    """)

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
✅ **Exercise:** Walk for 30-45 minutes daily  
✅ **Diet:** Eat high-fiber foods, vegetables, and fruits  
✅ **Hydration:** Drink 8-10 glasses of water daily  
✅ **Avoid:** Smoking, alcohol, sugary drinks  
✅ **Sugar:** Cut down on sweets and processed foods  
✅ **Sleep:** Get 7-8 hours of quality sleep  
✅ **Check-ups:** Regular health monitoring and blood tests  
✅ **Stress:** Practice meditation or yoga daily  
""")

st.write("---")
st.caption("Made with ❤️ using Streamlit & Machine Learning")