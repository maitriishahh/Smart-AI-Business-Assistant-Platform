import { useState } from "react";
import { useNavigate } from "react-router-dom";

import API from "../api/axios";

function Login() {

  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);



  // =========================================
  // HANDLE LOGIN
  // =========================================

  const handleLogin = async () => {

    if (!email || !password) {

      alert("Please fill all fields");

      return;
    }

    setLoading(true);

    try {

      const formData = new URLSearchParams();

      formData.append(
        "username",
        email
      );

      formData.append(
        "password",
        password
      );



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



      console.log("LOGIN RESPONSE:");

      console.log(response.data);



      // =========================================
      // SAVE TOKEN
      // =========================================

      localStorage.setItem(

        "token",

        response.data.access_token
      );



      // =========================================
      // REDIRECT
      // =========================================

      window.location.href = "/dashboard";



    } catch (error) {

      console.log(error);

      alert(
        error.response?.data?.detail ||
        "Login Failed"
      );

    } finally {

      setLoading(false);
    }
  };



  // =========================================
  // UI
  // =========================================

  return (

    <div className="
      flex
      items-center
      justify-center
      h-screen
      bg-slate-950
      text-white
    ">

      <div className="
        bg-slate-800
        p-10
        rounded-2xl
        w-[400px]
        shadow-2xl
      ">

        {/* Title */}

        <h1 className="
          text-4xl
          font-semi-bold
          mb-8
          text-center
        ">
          AI Business Assistant Platform
        </h1>



        {/* Email */}

        <input
          className="
            w-full
            p-4
            mb-4
            rounded-xl
            bg-slate-700
            outline-none
          "
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) =>
            setEmail(e.target.value)
          }
        />



        {/* Password */}

        <input
          className="
            w-full
            p-4
            mb-6
            rounded-xl
            bg-slate-700
            outline-none
          "
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />



        {/* Login Button */}

        <button
          className="
            w-full
            bg-blue-600
            hover:bg-blue-500
            transition
            p-4
            rounded-xl
            font-semibold
            disabled:opacity-50
          "
          onClick={handleLogin}
          disabled={loading}
        >

          {
            loading
              ? "Logging in..."
              : "Login"
          }

        </button>

      </div>

    </div>
  );
}

export default Login;