from marshmallow import Schema, fields, validate


class OTPRegisterVerifySchema(Schema):
    """
    Used to verify OTP
    """

    email = fields.Email(required=False)
    otp = fields.Str(required=True, validate=validate.Length(equal=6))


class OTPRegisterResendSchema(Schema):
    email = fields.Email(required=True)


class ForgotPasswordSchema(Schema):
    email = fields.Email(required=True)
    

class VerifyForgotOTPSchema(Schema):
    email = fields.Email(required=True)
    otp = fields.Str(required=True, validate=validate.Length(equal=6))
