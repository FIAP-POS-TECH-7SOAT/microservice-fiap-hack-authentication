import re

from marshmallow import Schema, fields, validates, ValidationError

class CreateUserRequestValidator(Schema):
    user_email = fields.Str(required=True)
    password = fields.Str(required=True)
    phone = fields.Str(required=False)

    @validates("user_email")
    def validate_email(self, user_email):
        obj = re.search(r'[\w.]+\@[\w.]+', user_email)
        if not obj:
            raise ValidationError("Invalid Email")
