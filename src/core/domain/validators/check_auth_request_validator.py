from marshmallow import Schema, fields
class CheckAuthRequestValidator(Schema):
    user_email = fields.Str(required=True)
    password = fields.Str(required=True)
