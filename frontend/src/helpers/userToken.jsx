const userToken = () => {
  const token = localStorage.getItem("token");
  if (token && token.length > 0) {
    return token;
  }
  return;
};

export default userToken;
