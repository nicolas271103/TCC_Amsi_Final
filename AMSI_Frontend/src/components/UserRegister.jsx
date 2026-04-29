import { useState } from "react";
import "../styles/userregister.css";
import { createUser } from "../services/api";

function UserRegister() {
  const [form, setForm] = useState({
    nome: "",
    email: "",
    senha: "",
    cargo: "",
    perfil: "",
  });

  const [erro, setErro] = useState("");
  const [sucesso, setSucesso] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setErro("");
    setSucesso("");

    try {
      await createUser({
        senha: form.senha,
        nome: form.nome,
        email: form.email,
        cargo: form.cargo,
        perfil_de_acesso: form.perfil,
        notificacao: false,
      });

      setSucesso("Usuário cadastrado com sucesso!");

      // limpa formulário
      setForm({
        nome: "",
        email: "",
        senha: "",
        cargo: "",
        perfil: "",
      });

    } catch (err) {
      console.log(err);
      setErro("Erro ao cadastrar usuário");
    }
  };

  return (
    <div className="container">
      <div className="box">
        <h2>Cadastro de Usuários</h2>

        <form onSubmit={handleSubmit}>
          <label>Nome Completo</label>
          <input
            name="nome"
            value={form.nome}
            onChange={handleChange}
          />

          <label>Email</label>
          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
          />

          <label>Senha</label>
          <input
            type="password"
            name="senha"
            value={form.senha}
            onChange={handleChange}
          />

          <label>Cargo</label>
          <select
            name="cargo"
            value={form.cargo}
            onChange={handleChange}
          >
            <option value="">Selecione</option>
            <option value="Diretor">Diretor</option>
            <option value="Tesoureiro">Tesoureiro</option>
            <option value="Secretario">Secretário</option>
          </select>

          <label>Perfil de Acesso</label>
          <select
            name="perfil"
            value={form.perfil}
            onChange={handleChange}
          >
            <option value="">Selecione</option>
            <option value="Administrador">Administrador</option>
            <option value="Usuario">Usuário</option>
          </select>

          <div className="buttons">
            <button
              type="button"
              className="cancel"
              onClick={() => {
                setForm({
                  nome: "",
                  email: "",
                  senha: "",
                  cargo: "",
                  perfil: "",
                });
              }}
            >
              Cancelar
            </button>

            <button type="submit" className="save">
              Salvar
            </button>
          </div>
        </form>

        {/* 🔥 feedback */}
        {erro && <p className="erro">{erro}</p>}
        {sucesso && <p className="sucesso">{sucesso}</p>}
      </div>
    </div>
  );
}

export default UserRegister;