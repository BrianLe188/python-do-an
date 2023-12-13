import "./App.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Login from "./pages/login";
import Home from "./pages/home";

function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <Home />,
    },
    {
      path: "/login",
      element: <Login />,
    },
    {
      path: "/register",
      element: <></>,
    },
  ]);

  return <RouterProvider router={router} />;
}

export default App;
