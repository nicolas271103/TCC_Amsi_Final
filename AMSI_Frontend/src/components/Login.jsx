import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";
import { loginUser } from "../services/api.js";
import { isAuthenticated } from "../services/auth.js";

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");

  // 🔐 Se já estiver logado, vai direto pra home
  useEffect(() => {
    if (isAuthenticated()) {
      navigate("/home");
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const data = await loginUser(email, senha);

      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));
      localStorage.setItem(
        "expiresAt",
        Date.now() + (data.expiresIn || 3600) * 1000
      );

      navigate("/home");
    } catch (err) {
      if (err instanceof Error) {
        setErro(err.message);
      } else {
        setErro("Erro inesperado");
      }

      setTimeout(() => setErro(""), 3000);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Login</h2>

        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Senha"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
          />

          <button type="submit">Entrar</button>

          {erro && <p style={{ color: "red" }}>{erro}</p>}
        </form>
      </div>
    </div>
  );
}

export default Login;