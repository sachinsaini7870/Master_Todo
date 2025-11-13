from marshmallow import Schema, fields, validate


class OTPRegisterVerifySchema(Schema):
    """
    Used to verify OTP
    """

    email = fields.Email(required=False)
    otp = fields.Str(required=True, validate=validate.Length(equal=6))
    purpose = fields.Str(required=True, validate=validate.OneOf(["register"]))


class OTPRegisterResendSchema(Schema):
    email = fields.Email(required=True)
    purpose = fields.Str(required=True, validate=validate.OneOf(["register"]))


class ForgotPasswordSchema(Schema):
    email = fields.Email(required=True)
    purpose = fields.Str(required=True, validate=validate.OneOf(["forgot"]))
    

class OTPForgotVerifySchema(OTPRegisterVerifySchema):
    purpose = fields.Str(required=True, validate=validate.OneOf(["forgot"]))


class VerifyForgotOTPSchema(Schema):
    email = fields.Email(required=True)
    otp = fields.Str(required=True, validate=validate.Length(equal=6))
    purpose = fields.Str(required=True, validate=validate.OneOf(["forgot"]))
