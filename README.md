# 🩺 Diabetes Prediction App

An intelligent web app built with **Streamlit** that predicts **diabetes risk**, includes **BMI** and **family history calculators**, and generates **personalized PDF health reports**.
## 🚀 Live Project

🔗 **Access the deployed app here:** 👉 [Click to Open](https://diabetespredictor-hmrrv.streamlit.app/)

## 📋 Setup Steps

### Step 1: Train the Model (First Time Only)
```bash
pip install -r requirements.txt
```

Open and run `code.ipynb` (or your notebook name) to generate:
- `model_rf.joblib`
- `scaler.joblib`

### Step 2: Run the App
```bash
streamlit run app.py
```



## 📁 Project Files
```
├── app.py                    # Main app
├── code.ipynb      # Train model (run this first!)
├── requirements.txt          # All packages
├── model_rf.joblib          # Generated after training
└── scaler.joblib            # Generated after training
```

## How to Use

1. **Calculators** → Calculate BMI & family risk
2. **Predict** → Enter health data
3. **Download** → Get PDF report

## Features

✅ Diabetes risk prediction  
✅ BMI calculator  
✅ Family history estimator  
✅ PDF health reports  
✅ Health tips & info  

## Dataset

Model trained on: [(https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database)]



## ⚠️ Important Notes

- Run the `.ipynb` notebook **first** to create model files
- The `.joblib` files are **required** for the app to work
- This is a **screening tool**, not a diagnosis

## Acknowledgment

This project adapts code from [https://github.com/viochris/Diabetes-prediction-project.git]
(Diabetes-prediction-project by viochris,licensed under the MIT License.)
Special thanks to the original author for their open-source contribution. 🙌

## Made With

Python • Streamlit • Machine Learning • Jupyter

---

⭐ Star if helpful!