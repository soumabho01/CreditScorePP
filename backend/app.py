from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pickle

app = Flask(__name__)
CORS(app)

DB_NAME = "users.db"

# ✅ Load trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# ✅ Categorical mappings (must match training encodings!)
education_map = {"Graduate": 0, "Not Graduate": 1}
employment_map = {"Salaried": 0, "Self-Employed": 1}
marital_map = {"Single": 0, "Married": 1}
loanpurpose_map = {"Auto": 0, "Home": 1, "Education": 2, "Personal": 3}  # adjust if needed

# ✅ Ensure users table exists
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    finally:
        conn.close()

    return jsonify({"message": "Signup successful"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    try:
        features = [
            int(data["Age"]),
            float(data["Income"]),
            float(data["LoanAmount"]),
            float(data["CreditScore"]),
            int(data["MonthsEmployed"]),
            int(data["NumCreditLines"]),
            float(data["InterestRate"]),
            int(data["LoanTerm"]),
            float(data["DTIRatio"]),
            int(data["HasMortgage"]),
            int(data["HasDependents"]),
            int(data["HasCoSigner"]),
            education_map.get(data["Education"], 0),         # default 0 if not found
            employment_map.get(data["EmploymentType"], 0),   # default 0
            marital_map.get(data["MaritalStatus"], 0),       # default 0
            loanpurpose_map.get(data["LoanPurpose"], 0)      # default 0
        ]

        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0][1]
        prediction_label = "Default" if prediction == 1 else "No Default"

        return jsonify({
            "prediction": prediction_label,
            "default_probability": float(probability)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    init_db()  # ✅ Makes sure the table exists before running
    app.run(debug=True)


