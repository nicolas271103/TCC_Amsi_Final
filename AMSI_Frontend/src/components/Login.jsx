import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";
import { loginUser } from "../services/api.js";

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");


  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Login</h2>

        <form onSubmit={async (e) => {
          e.preventDefault();
          try {
            await loginUser(email, senha);
            navigate("/home");
          } catch (err) {
            setErro(err.message);

            setTimeout(() => {
              setErro("");
            }, 3000);
          }
        }}>
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
        </form>
        {erro && <p className="erro">{erro}</p>}
      </div>
    </div>
  );
}

export default Login;