import { Navigate, Route, Routes } from "react-router-dom";

import { useAuth } from "./lib/useAuth";
import { AuthPage } from "./routes/AuthPage";
import { TodoApp } from "./routes/TodoApp";

function ProtectedRoute() {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <TodoApp /> : <Navigate to="/login" replace />;
}

function GuestRoute({ mode }: { mode: "login" | "register" }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <Navigate to="/" replace /> : <AuthPage mode={mode} />;
}

export function App() {
  return (
    <Routes>
      <Route path="/" element={<ProtectedRoute />} />
      <Route path="/login" element={<GuestRoute mode="login" />} />
      <Route path="/register" element={<GuestRoute mode="register" />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
