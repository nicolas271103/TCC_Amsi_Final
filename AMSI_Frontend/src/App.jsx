import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import HomePage from "./components/Home";
import UserRegisterPage from "./pages/UserRegisterPage";
import UserListPage from "./pages/UserListPage";
import ClientRegisterPage from "./pages/ClientRegisterPage";
import LancamentoPage from "./pages/LancamentoPage";
import ListaLancamentosPage from "./pages/ListaLancamentosPage";
import PrivateRoute from "./components/PrivateRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* rota pública */}
        <Route path="/" element={<LoginPage />} />

        {/* rotas protegidas */}
        <Route
          path="/home"
          element={
            <PrivateRoute>
              <HomePage />
            </PrivateRoute>
          }
        />

        <Route
          path="/cadastro"
          element={
            <PrivateRoute>
              <UserRegisterPage />
            </PrivateRoute>
          }
        />

        <Route
          path="/usuarios"
          element={
            <PrivateRoute>
              <UserListPage />
            </PrivateRoute>
          }
        />

        <Route
          path="/cliente_fornecedor"
          element={
            <PrivateRoute>
              <ClientRegisterPage />
            </PrivateRoute>
          }
        />

        <Route
          path="/lancamento"
          element={
            <PrivateRoute>
              <LancamentoPage />
            </PrivateRoute>
          }
        />

        <Route
          path="/tipo_lancamento"
          element={
            <PrivateRoute>
              <ListaLancamentosPage />
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;