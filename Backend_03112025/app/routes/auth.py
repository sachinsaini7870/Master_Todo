from flask import request  # To access incoming JSON payloads

from flask_restx import (
    Namespace,
    Resource,
)  # For creating namespaces, RESTful resources, and Swagger models

from marshmallow import (
    ValidationError,
)  # To handle validation errors from Marshmallow schemas

from ..schemas.auth_schema import (
    RegisterSchema,
    LoginSchema,
    ResetPasswordSchema,
    ChangePasswordSchema,
)  # Marshmallow schemas for validating register/login input


from ..schemas.otp_schema import (
    OTPRegisterVerifySchema,
    OTPRegisterResendSchema,
    ForgotPasswordSchema,
)

from ..services.auth_service import (
    login_user,
    register_user,
    resend_register_otp_service,
    verify_register_otp_service,
    forgot_service,
    reset_password_service,
    change_password_service,
)

from flask_jwt_extended import jwt_required, get_jwt  # For JWT authentication


from ..swagger_models.auth_models import swagger_auth_models


# Create a Namespace for authentication routes
# This groups related routes together and adds descriptions for Swagger docs
auth_ns = Namespace("auth", description="Authentication operations")


# Register Swagger models
(
    register_model,
    login_model,
    otp_register_verify_model,
    otp_register_resend_model,
    forgot_model,
    reset_password_model,
    change_password_model,
) = swagger_auth_models(auth_ns)


# /register Route
@auth_ns.route("/register")
class Register(Resource):
    # Expect the register_model for Swagger documentation and validate automatically
    @auth_ns.expect(register_model, validate=True)
    def post(self):
        """
        POST /auth/register
        1. Validate incoming JSON using Marshmallow schema
        2. If validation fails, return 400 with error messages
        3. Otherwise, call service function to register user
        """
        try:
            # Load and validate incoming JSON data
            data = RegisterSchema().load(request.json)
        except ValidationError as err:
            # Return validation errors with HTTP 400
            return {"errors": err.messages}, 400
        # Call the service layer to register the user
        return register_user(data)


# /login Route
@auth_ns.route("/login")
class Login(Resource):
    # Expect the login_model for Swagger documentation and validate automatically
    @auth_ns.expect(login_model, validate=True)
    def post(self):
        """
        POST /auth/login
        1. Validate incoming JSON using Marshmallow schema
        2. If validation fails, return 400 with error messages
        3. Otherwise, call service function to login user
        """
        try:
            # Load and validate incoming JSON data
            data = LoginSchema().load(request.json)
        except ValidationError as err:
            # Return validation errors with HTTP 400
            return {"errors": err.messages}, 400
        # Call the service layer to log in the user and return token or response
        return login_user(data)


@auth_ns.route("/resend-registration-otp")
class ResendRegistrationOTP(Resource):
    @auth_ns.expect(otp_register_resend_model, validate=True)
    def post(self):
        try:
            data = OTPRegisterResendSchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        return resend_register_otp_service(data)


@auth_ns.route("/verify-register-otp")
class VerifyRegistrationOTP(Resource):
    @auth_ns.expect(otp_register_verify_model, validate=True)
    def post(self):
        try:
            data = OTPRegisterVerifySchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400
        return verify_register_otp_service(data)


@auth_ns.route("/forgot-password")
class ForgotPassword(Resource):
    @auth_ns.expect(forgot_model, validate=True)
    def post(self):
        try:
            data = ForgotPasswordSchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        return forgot_service(data)


@auth_ns.route("/reset-password")
class ResetPassword(Resource):
    @auth_ns.expect(reset_password_model, validate=True)
    def post(self):
        try:
            data = ResetPasswordSchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        return reset_password_service(data)

@auth_ns.route("/change-password")
class ChangePassword(Resource):
    @jwt_required()
    @auth_ns.expect(change_password_model, validate=True)
    def post(self):
        try:
            data = ChangePasswordSchema().load(request.json)
            claims = get_jwt()
            email=claims.get("email")
        except ValidationError as err:
            return {"errors": err.messages}, 400

        return change_password_service(data, email)
