const BASE_URL = import.meta.env.VITE_API_URL;

// ======================
// 🔐 LOGIN
// ======================
export const loginUser = async (email, senha) => {
  const response = await fetch(`${BASE_URL}/https://amsi-project-chzs.vercel.app/auth/token/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "ngrok-skip-browser-warning": "true",
    },
    body: JSON.stringify({
      login: email,
      senha: senha,
      id_usuario_fk: 0,
      dispositivo_logado: "Desktop",
      localizacao: "Brasil",
      navegador: navigator.userAgent,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Usuário inválido");
  }

  return await response.json();
};

// ======================
// 👤 CRIAR USUÁRIO
// ======================
export const createUser = async (data) => {
  const response = await fetch(`${BASE_URL}/usuarios/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "ngrok-skip-browser-warning": "true",
    },
    body: JSON.stringify({
      login: data.login,
      senha: data.senha,
      nome: data.nome,
      email: data.email,
      cargo: data.cargo,
      perfil_de_acesso: data.perfil,
      notificacao: false,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(JSON.stringify(error.detail || "Erro ao criar usuário"));
  }

  return await response.json();
};

// ======================
// 📋 LISTAR USUÁRIOS
// ======================
export const getUsers = async () => {
  const response = await fetch(`${BASE_URL}/usuarios/`, {
    headers: {
      "ngrok-skip-browser-warning": "true",
    },
  });

  if (!response.ok) {
    throw new Error("Erro ao buscar usuários");
  }

  return await response.json();
};

export const getNews = async () => {
  const response = await fetch("https://prefeitura.sp.gov.br/web/sao_miguel_paulista");
  return await response.json();
};