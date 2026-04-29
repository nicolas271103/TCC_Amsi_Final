import { useEffect, useState } from "react";
import "../styles/home.css";
import News from "./News";

function Home() {
  return (
    <div className="home-container">
      <h1>Bem-vindo ao sistema</h1>
      <p>Você está logado</p>

      <div className="cards">
        <div className="card">Usuários</div>
        <div className="card">Relatórios</div>
        <div className="card">Configurações</div>
        <div className="button">Lançamentos</div>
      </div>

        <div className="card" onClick={() => navigate("/lancamento")}>
            <h3>Lançamentos</h3>
          <p>Cadastrar e gerenciar</p>
        </div>

      <News />
    </div>
  );
}

export default Home;