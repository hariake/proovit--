import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/useAuth";
import api from "../api/client";

export default function Login() {
    const { login } = useAuth();
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");


    // On form submit, sends login request to backend, if successful, saves user and token to context and localStorage through login function from AuthContext, then redirects to dashboard. If login fails, shows error message.
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const res = await api.post("/api/login", { username, password });
            login({ user_id: res.data.user_id, username: res.data.username }, res.data.token);
            navigate("/")
            } catch {
                setError("Invalid username or password");   
            }
    };

    return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded shadow w-full max-w-sm">
        <h1 className="text-2xl font-bold mb-6">Login</h1>
        {error && <p className="text-red-500 mb-4">{error}</p>}  {/* Shows error message if there is an error */}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input 
            className="border rounded p-2"
            placeholder="Username"
            value={username}
            onChange={e => setUsername(e.target.value)}
          />
          <input 
            className="border rounded p-2"
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
          />
          <button className="bg-blue-600 text-white rounded p-2 hover:bg-blue-700">
            Login
          </button>
        </form>
        <p className="mt-4 text-sm text-center">
          No account? <Link to="/register" className="text-blue-600 hover:underline">Register</Link>
        </p>
      </div>
    </div>
  )
}