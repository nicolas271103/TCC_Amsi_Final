import {BrowserRouter, Routes, Route} from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import HomePage from "./components/Home"
import UserRegisterPage from "./pages/UserRegisterPage";
import UserListPage from "./pages/UserListPage";
import ClientRegisterPage from "./pages/ClientRegisterPage";
import LancamentoPage from "./pages/LancamentoPage";
import ListaLancamentosPage from "./pages/ListaLancamentosPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/cadastro" element ={<UserRegisterPage />} />
        <Route path="/usuarios" element ={<UserListPage/>} />
        <Route path="/cliente_fornecedor" element = {<ClientRegisterPage/>} />
        <Route path="/lancamento" element={<LancamentoPage />} />
        <Route path="/tipo_lancamento" element={<ListaLancamentosPage />} />
      
      </Routes>
    </BrowserRouter>
  );
}

export default App;