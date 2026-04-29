import users from "../mock/users.json";

export async function loginUser(email, senha) {
  await new Promise((r) => setTimeout(r, 500));

  const user = users.find(
    (u) => u.email === email && u.senha === senha
  );

  if (!user) {
    throw new Error("Usuário inválido");
  }

  return {
    token: "fake-token",
    user
  };
}

export const getUsers = async () => {
  const response = await fetch(`${BASE_URL}/usuarios/`, {
    headers: {
      "ngrok-skip-browser-warning": "true"
    }
  });

  if (!response.ok) {
    throw new Error("Erro ao buscar usuários");
  }

  return await response.json();
};

export const getNews = async () => {
  const response = await fetch(
    `https://prefeitura.sp.gov.br/web/sao_miguel_paulista/`
  );

  const data = await response.json();
  return data.articles;
};