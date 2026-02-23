import { useContext } from "react";
import { AuthContext } from "./AuthContext";

// hook for other components to get the auth object.

export const useAuth = () => {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
    return ctx;
};