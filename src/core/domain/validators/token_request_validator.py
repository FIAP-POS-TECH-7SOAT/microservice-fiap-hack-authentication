from marshmallow import Schema, fields

class TokenValidator(Schema):
    token = fields.Str(required=True)
