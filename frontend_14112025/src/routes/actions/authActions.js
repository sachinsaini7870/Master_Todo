import { redirect } from "react-router-dom";
import { changePasswordApi, loginApi, resendRegisterOtpApi, resetPasswordApi, sendForgotApi, sendRegisterOtpApi, verifyRegisterOtpApi } from "../../api";


export async function loginAction({ request }) {
    try {
        const formData = await request.formData();

        const payload = {
            email: formData.get("email"),
            password: formData.get("password"),
        };

        const res = await loginApi(payload);

        if (res.token && res.user) {
            localStorage.setItem("token", res.token);
            localStorage.setItem("user", res.user);

            return redirect("/todos/list");
        }

    } catch (error) {
        const message = error.response?.data?.error || "Something went wrong, try again.";

        return {
            success: false,
            error: message,
        };
    }
}


export async function sendRegisterOtpAction({ request }) {
    const formData = await request.formData();

    const payload = {
        username: formData.get("username"),
        email: formData.get("email"),
        password: formData.get("password"),
    };

    const res = await sendRegisterOtpApi(payload);

    if (res.user_email) {
        localStorage.setItem("email", res.user_email);
        return redirect("/auth/verify-signup");
    }

    return { success: false, message: res.error };
}

export async function reSendRegisterOtpAction({ request }) {
    try {
        const formData = await request.formData();

        const payload = { email: formData.get("email") };

        const res = await resendRegisterOtpApi(payload);

        return { success: true, message: res.message };

    } catch (error) {
        const message = error.response?.data?.error || "Something went wrong, try again.";

        return {
            success: false,
            error: message,
        };
    }
}

export async function verifyRegisterOtpAction({ request }) {

    try {
        const formData = await request.formData();
        const email = formData.get("email")
        let payload;

        if (email) {
            payload = {
                email: formData.get("email"),
                otp: formData.get("otp"),
            };
        }
        else {
            payload = {
                email: localStorage.getItem("email"),
                otp: formData.get("otp"),
            };
        }

        const res = await verifyRegisterOtpApi(payload);

        const user = res.username
        const token = res.token

        localStorage.setItem("token", token);
        localStorage.setItem("user", `"${user}"`);
        localStorage.removeItem("email");

        return redirect("/");

    } catch (error) {
        const message = error.response?.data?.error || "Something went wrong, try again.";

        return {
            success: false,
            error: message,
        };
    }
}


export async function forgotAction({ request }) {
    try {
        const formData = await request.formData();

        const payload = { email: formData.get("email") };

        const res = await sendForgotApi(payload);

        return { success: true, message: res.message };

    } catch (error) {
        const message = error.response?.data?.error || "Something went wrong, try again.";

        return {
            success: false,
            error: message,
        };
    }
}


export async function restPasswordAction({ request, params }) {
    try {
        const formData = await request.formData();

        const payload = {
            token: params.token,
            password: formData.get("password")
        };

        await resetPasswordApi(payload);

        // return { success: true, message: res.message };
        return redirect("/auth/login");

    } catch (error) {
        const message = error.response?.data?.error || "Something went wrong, try again.";

        return {
            success: false,
            error: message,
        };
    }
}


export async function changePasswordAction({ request }) {
    try {

        const formData = await request.formData();



        const payload = {
            old_password: formData.get("old_password"),
            new_password: formData.get("new_password")
        };

        await changePasswordApi(payload);

        // return { success: true, message: res.message };
        return redirect("/todos/list");

    } catch (error) {
        const message = error.response?.data?.error || "Something went wrong, try again.";

        return {
            success: false,
            error: message,
        };
    }
}


