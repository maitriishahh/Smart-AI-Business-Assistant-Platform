import { useState } from "react";
import { useNavigate } from "react-router-dom";

import API from "../api/axios";

function Login() {

  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {

  try {

    const formData = new URLSearchParams();

    formData.append("username", email);
    formData.append("password", password);

    const response = await API.post(
      "/auth/login",
      formData,
      {
        headers: {
          "Content-Type":
            "application/x-www-form-urlencoded"
        }
      }
    );

    localStorage.setItem(
      "token",
      response.data.access_token
    );

    navigate("/dashboard");

  } catch (error) {

    console.log(error);

    alert("Login Failed");
  }
};

  return (

    <div className="flex items-center justify-center h-screen">

      <div className="bg-slate-800 p-8 rounded-2xl w-96 shadow-lg">

        <h1 className="text-3xl font-bold mb-6 text-center">
          Login
        </h1>

        <input
          className="w-full p-3 mb-4 rounded bg-slate-700"
          type="email"
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          className="w-full p-3 mb-4 rounded bg-slate-700"
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          className="w-full bg-blue-600 p-3 rounded-lg"
          onClick={handleLogin}
        >
          Login
        </button>

      </div>

    </div>
  );
}

export default Login;