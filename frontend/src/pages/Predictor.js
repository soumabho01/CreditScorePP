import React, { useState } from "react";
import axios from "axios";
import "../App.css"; // use the same CSS styling

function Predictor() {
  const [formData, setFormData] = useState({
    LoanID: "",
    Age: "",
    Income: "",
    LoanAmount: "",
    CreditScore: "",
    MonthsEmployed: "",
    NumCreditLines: "",
    InterestRate: "",
    LoanTerm: "",
    DTIRatio: "",
    Education: "Graduate",
    EmploymentType: "Salaried",
    MaritalStatus: "Single",
    HasMortgage: "0",
    HasDependents: "0",
    LoanPurpose: "Auto",
    HasCoSigner: "0",
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://127.0.0.1:5000/predict", formData);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setResult({ error: "Something went wrong" });
    }
  };

  return (
    <div className="container">
      <h1 className="title">CreditScore++ Predictor</h1>
      <form onSubmit={handleSubmit} className="form">
        {Object.keys(formData).map((key) => (
          <div key={key} className="form-group">
            <label>{key}</label>
            {["Education", "EmploymentType", "MaritalStatus", "LoanPurpose"].includes(key) ? (
              <select name={key} value={formData[key]} onChange={handleChange}>
                {key === "Education" &&
                  ["Graduate", "Not Graduate", "High School"].map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                {key === "EmploymentType" &&
                  ["Salaried", "Self-Employed", "Unemployed"].map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                {key === "MaritalStatus" &&
                  ["Single", "Married", "Divorced"].map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                {key === "LoanPurpose" &&
                  ["Auto", "Home", "Education", "Personal"].map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
              </select>
            ) : (
              <input
                type="text"
                name={key}
                value={formData[key]}
                onChange={handleChange}
              />
            )}
          </div>
        ))}
        <button type="submit" className="btn">Predict</button>
      </form>

      {result && (
  <div
    className={`result-card ${
      parseFloat(result.default_probability) < 0.5 ? "Good" : "Bad"
    }`}
  >
    <h2>Prediction Result</h2>
    <p>
      <strong>Prediction:</strong>{" "}
      {parseFloat(result.default_probability) < 0.5 ? "Good" : "Bad"}
    </p>
    <p>
      <strong>Default Probability:</strong> {result.default_probability}
    </p>
  </div>
)}

    </div>
  );
}

export default Predictor;
