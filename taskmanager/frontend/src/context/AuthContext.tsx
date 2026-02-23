import { createContext, useState, type ReactNode } from "react";

// Define the shape of a user
interface User {
    user_id: number;
    username: string;
}

// Define the shape of the AuthContext, for developer convenience, catches type errors early
interface AuthContextType {
    user: User | null;
    token: string | null;
    login: (user: User, token: string) => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null) // creates an empty context container

export function AuthProvider({ children }: { children: ReactNode }) {  // Provides the context to the app, wraps around the app in main.tsx
    const [user, setUser] = useState<User | null>(() => { // Initializes user state from localStorage, if it exists, keeps user logged in across page refreshes
        const stored = localStorage.getItem("user");
        return stored ? JSON.parse(stored) : null;
    });
    const [token, setToken] = useState<string | null>(() => // Initializes token state from localStorage, if it exists, keeps token across page refreshes
        localStorage.getItem("token"));

    const login = (userData : User, token: string) => {  // On login, saves user and token to localStorage and updates React state(UI realizes there is a user logged in)
        localStorage.setItem("user", JSON.stringify(userData));    
        localStorage.setItem("token", token);
        setUser(userData);
        setToken(token);
    };

    const logout = () => { // On logout, clears localStorage and resets user and token state, UI realizes there is no user logged in
        localStorage.clear();
        setUser(null);
        setToken(null);
    };

    //provides the context value to the app, any component wrapped in AuthProvider can access user, token, login and logout through useAuth hook. we will wrap the whole App in main.tsx with AuthProvider so that the auth context is available throughout the app.
    return (
        <AuthContext.Provider value={{ user, token, login, logout }}> 
            {children}
        </AuthContext.Provider>
    );
}

export { AuthContext };