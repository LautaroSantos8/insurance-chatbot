import React from "react";
import * as ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Error from "./pages/Error.jsx";
import LogIn from "./pages/LogIn.jsx";
import SignUp from "./pages/SignUp.jsx";
import ProtectedRoute from "./auth/protectRoutes.jsx";
import { QuestionContextProvider } from "./context/chatContext";
import { MenuContextProvider } from "./context/LateralMenuContext.jsx";
import { QuickSearchProvider } from "./context/quickSearchContext.jsx";
import Chat from "./pages/Chat.jsx";
import Home from "./pages/Home.jsx";
import { Navigate } from "react-router-dom";
import "./index.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Navigate to="/home" />,
    errorElement: <Error />,
  },
  {
    path: "/home",
    element: <Home />,
  },
  {
    path: "/chat",
    element: (
      <ProtectedRoute>
        <Chat />
      </ProtectedRoute>
    ),
  },

  {
    path: "/log-in",
    element: <LogIn />,
  },
  {
    path: "/sign-up",
    element: <SignUp />,
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <QuickSearchProvider>
      <MenuContextProvider>
        <QuestionContextProvider>
          <RouterProvider router={router} />
        </QuestionContextProvider>
      </MenuContextProvider>
    </QuickSearchProvider>
  </React.StrictMode>
);
