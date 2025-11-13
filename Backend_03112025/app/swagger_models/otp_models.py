from flask_restx import fields


def swagger_otp_models(ns):
    otp_register_verify_model = ns.model(
        "OtpVerify",
        {
            "email": fields.String(
                description="Email for OTP verification",
                default="sachin123@gmail.com",
            ),
            "otp": fields.String(
                required=True, description="6-digit OTP", default="123456"
            ),
            "purpose": fields.String(
                required=True,
                default="register",
                enum=["register"],
                description="only 'register' supported for this endpoint",
            ),
        },
    )

    otp_register_resend_model = ns.model(
        "OtpResend",
        {
            "email": fields.String(required=True, default="sachin123@gmail.com"),
            "purpose": fields.String(required=True, enum=["register"]),
        },
    )

    forgot_model = ns.model(
        "ForgotPassword",
        {
            "email": fields.String(required=True, default="sachin123@gmail.com"),
            "purpose": fields.String(required=True, enum=["forgot"], default="forgot"),
            
        },
    )

    forgot_verify_model = ns.model(
        "VerifyForgotOtp",
        {
            "email": fields.String(required=True, default="sachin123@gmail.com"),
            "otp": fields.String(required=True, default="123456"),
            "purpose": fields.String(required=True, enum=["forgot"], default="forgot"),
        },
    )

    reset_password_model = ns.model(
        "ResetPassword",
        {
            "email": fields.String(required=True, default="sachin123@gmail.com"),
            "new_password": fields.String(required=True, default="Sachin@123"),
        },
    )

    return (
        otp_register_verify_model,
        otp_register_resend_model,
        forgot_model,
        forgot_verify_model,
        reset_password_model,
    )
