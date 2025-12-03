import { redirect } from "react-router-dom";

export async function protectedLoader() {
    const token = localStorage.getItem("token");
    if (!token) {
        return redirect("/auth/login");
    }
    return null; 
}
