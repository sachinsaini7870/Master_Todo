import { Login, Signup, Forgot } from "../Modules/auth/";
import RootError from "../Modules/components/RootError";
import { redirect } from "react-router-dom";
import AuthLayout from "../Modules/layouts/AuthLayout";
import { forgotAction, reSendRegisterOtpAction, restPasswordAction, sendRegisterOtpAction, verifyRegisterOtpAction } from "./actions/authActions";
import VerifySignUp from "../Modules/auth/VerifySignUp";
import ResetPassword from "../Modules/auth/ResetPassword";


export const AuthRoutes = [

    {
        path: "auth",
        Component: AuthLayout,
        ErrorBoundary: RootError,
        children: [
            { index: true, loader: () => redirect("./login") },
            { path: "login", Component: Login },

            { path: "signup", Component: Signup, action: sendRegisterOtpAction, },
            { path: "verify-signup", Component: VerifySignUp, action: verifyRegisterOtpAction },
            { path: "resend-otp", action: reSendRegisterOtpAction },

            { path: "forgot", Component: Forgot, action: forgotAction },
            { path: "reset-password/:token", Component: ResetPassword, action: restPasswordAction }

        ]
    }
]