# CreditScore++ – Explainable Creditworthiness Engine

CreditScore++ is a machine learning–powered web application that predicts **loan default risk** based on user financial and demographic data.  
It combines a **React frontend** with a **Flask backend** and a **RandomForestClassifier model** trained on loan default data.  

---

##  Features

-  **Authentication System** (Signup/Login with SQLite database)
- **Credit Risk Prediction** using a trained ML model
-  **Clean & Responsive UI** built with React
- **Visual Feedback**  
  - Green card → "No Default"  
  - Red card → "Default"
-  **Custom Threshold** (configurable, currently `0.41`)
-  Full-stack integration (Flask REST API + React client)

---

## 🛠️ Tech Stack

- **Frontend**: React.js, Axios, CSS  
- **Backend**: Flask, SQLite, scikit-learn  
- **Machine Learning**: RandomForestClassifier  
- **Dataset**: Loan Default dataset (`Loan_default.csv`)  

---

## Project Structure
CreditScorePP/
├── backend/
│ ├── app.py # Flask backend (API + model serving)
│ ├── model.pkl # Trained RandomForest model
│ ├── train_model.py # Script to train & save model
│ ├── users.db # SQLite database (auto-created)
│
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ │ └── Predictor.js 
      ---Signup.js
      ---Login.js
│ │ ├── App.css
│ │ └── App.js
│ ├── package.json
│
├── Loan_default.csv 
├── README.md 



