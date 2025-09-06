import React from "react";
import { useNavigate, Link } from "react-router-dom";
import AuthForm from "../components/AuthForm";

const Login = () => {
  const navigate = useNavigate();

  const handleLogin = async ({ email, password }) => {
    const res = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) throw new Error("Login failed");
    navigate("/predictor");
  };

  return (
    <div>
      <AuthForm type="login" onSubmit={handleLogin} />
      <p style={{ textAlign: "center", marginTop: "10px" }}>
        Don’t have an account? <Link to="/">Signup here</Link>
      </p>
    </div>
  );
};

export default Login;


