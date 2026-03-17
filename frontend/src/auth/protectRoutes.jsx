import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem("token");

  if (token !== null) {
    return children;
  } else {
    return <Navigate to="/home" />;
  }
};

export default ProtectedRoute;
