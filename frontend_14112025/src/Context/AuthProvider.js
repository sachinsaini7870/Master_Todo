import React, { useState, useEffect, useCallback } from "react";
import { AuthContext } from "./AuthContext";
import { authStorage } from "../utils/authStorage";

export function AuthProvider({ children }) {
    const [token, setToken] = useState(() => authStorage.getToken());
    const [user, setUser] = useState(() => authStorage.getUser());

    // Restore auth once when app loads
    useEffect(() => {
        const storedToken = authStorage.getToken();
        const storedUser = authStorage.getUser();
        if (storedToken) setToken(storedToken);
        if (storedUser) setUser(storedUser);
    }, []);

    // Login
    const login = useCallback((tokenValue, userValue) => {
        authStorage.setToken(tokenValue);
        authStorage.setUser(userValue);

        setToken(tokenValue);
        setUser(userValue);
    }, []);

    // Logout
    const logout = useCallback(() => {
        authStorage.removeToken();
        authStorage.removeUser();
        authStorage.removeAll();

        setToken(null);
        setUser(null);
    }, []);

    const isAuthenticated = !!token;

    const value = {
        token,
        user,
        isAuthenticated,
        login,
        logout,
        setToken,
        setUser
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
