import { useAuth } from "../context/useAuth";

export default function Dashboard() {
    const { user, logout } = useAuth(); // Gets user and logout function from auth context using useAuth hook

     return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold">Welcome, {user?.username}</h1>
        <button
          onClick={logout}
          className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
        >
          Logout
        </button>
      </div>
      <p className="text-gray-500">Kanban board coming soon...</p>
    </div>
  )
}