from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/")
def home():
    return "✅ CreditScore++ API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json  # JSON input from frontend

        # Convert input into DataFrame
        df = pd.DataFrame([data])

        # Encode categorical columns (same as training)
        categorical_cols = ["Education", "EmploymentType", "MaritalStatus",
                            "HasMortgage", "HasDependents", "LoanPurpose", "HasCoSigner"]

        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype("category").cat.codes

        # Drop LoanID if passed
        if "LoanID" in df.columns:
            df = df.drop(columns=["LoanID"])

        # Predict
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1]  # probability of default
        result = "Good" if prediction == 0 else "Bad"

        return jsonify({
            "prediction": result,
            "default_probability": round(probability, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
