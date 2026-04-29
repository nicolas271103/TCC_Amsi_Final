export const isAuthenticated = () => {
  const token = localStorage.getItem("token");
  const expiresAt = localStorage.getItem("expiresAt");

  if (!token || !expiresAt) return false;

  if (Date.now() > Number(expiresAt)) {
    logout();
    return false;
  }

  return true;
};

export const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  localStorage.removeItem("expiresAt");
};