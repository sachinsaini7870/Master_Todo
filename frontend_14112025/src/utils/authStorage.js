export const authStorage = {
    getToken: () => localStorage.getItem("token"),
    setToken: (t) => localStorage.setItem("token", t),
    removeToken: () => localStorage.removeItem("token"),
    removeAll: () => localStorage.clear(),

    getUser: () => JSON.parse(localStorage.getItem("user") || "null"),
    setUser: (u) => localStorage.setItem("user", JSON.stringify(u)),
    removeUser: () => localStorage.removeItem("user"),
};
