const destroySession = () => {
  localStorage.removeItem("token");
  window.location.assign("/home");
};

export default destroySession;
