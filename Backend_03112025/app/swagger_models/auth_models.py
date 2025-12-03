# Backend_03112025\app\swagger_models\auth_models.py
from flask_restx import fields


# -------------------------------
# Swagger Models (for API documentation only)
# -------------------------------
# These models define the expected input fields for Swagger UI and automatic validation
def swagger_auth_models(ns):
    """Swagger models for auth"""

    register_model = ns.model(
        "Register",
        {
            "username": fields.String(
                required=True, default="example123", description="e.g. example123"
            ),  # Required username field
            "email": fields.String(
                required=True,
                default="example123@gmail.com",
                description="e.g. example123@gmail.com",
            ),  # Required email field
            "password": fields.String(
                required=True, default="example@123", description="e.g. example@123"
            ),  # Required password field
        },
    )

    login_model = ns.model(
        "Login",
        {
            "email": fields.String(
                required=True,
                default="example123@gmail.com",
                description="e.g. example123@gmail.com",
            ),  # Required email field
            "password": fields.String(
                required=True, default="example@123", description="e.g. example@123"
            ),  # Required password field
        },
    )

    otp_register_verify_model = ns.model(
        "OtpVerify",
        {
            "email": fields.String(
                description="Email for OTP verification",
                default="example123@gmail.com",
            ),
            "otp": fields.String(
                required=True, description="6-digit OTP", default="123456"
            ),
        },
    )

    otp_register_resend_model = ns.model(
        "OtpResend",
        {
            "email": fields.String(required=True, default="example123@gmail.com"),
        },
    )

    forgot_model = ns.model(
        "ForgotPassword",
        {"email": fields.String(required=True, default="example123@gmail.com")},
    )

    reset_password_model = ns.model(
        "ResetPassword",
        {
            "token": fields.String(required=True),
            "password": fields.String(required=True, default="example@123"),
        },
    )

    change_password_model = ns.model(
        "ChangePassword",
        {
            "old_password": fields.String(required=True),
            "new_password": fields.String(required=True, default="example@123"),
        },
    )

    return (
        register_model,
        login_model,
        otp_register_verify_model,
        otp_register_resend_model,
        forgot_model,
        reset_password_model,
        change_password_model,
    )
