import { useNavigate } from "react-router-dom";
import { logout } from "../services/auth";

function Home() {
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <div>
      <h1>Home</h1>

      <button onClick={handleLogout}>
        Sair
      </button>
    </div>
  );
}

export default Home;