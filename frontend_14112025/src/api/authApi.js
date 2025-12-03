import api from "./api";

const auth = "/api/auth"


// Login Api's ......................
export async function loginApi({ email, password }) {
    const res = await api.post(auth + "/login", { email, password });
    return res.data; // { token, user: {...} }    
}


// Register Api's ......................
export async function sendRegisterOtpApi(data) {
    const res = await api.post(auth + "/register", data);
    return res.data;
}

export async function resendRegisterOtpApi(data) {
    const res = await api.post(auth + "/resend-registration-otp", data);
    return res.data;
}

export async function verifyRegisterOtpApi(data) {
    const res = await api.post(auth + "/verify-register-otp", data);
    return res.data;
}


// Forgot Api's ......................
export async function sendForgotApi(data) {
    const res = await api.post(auth + "/forgot-password", data);
    return res.data;
}

export async function resetPasswordApi(data) {
    const res = await api.post(auth + "/reset-password", data);
    return res.data;
}

export async function changePasswordApi(data) {
    const res = await api.post(auth + "/change-password", data);
    return res.data;
}
