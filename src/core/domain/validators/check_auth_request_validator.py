import re

from marshmallow import Schema, fields, validates, ValidationError

class CheckAuthRequestValidator(Schema):
    user_email = fields.Str(required=True)
    password = fields.Str(required=True)

    @validates("user_email")
    def validate_email(self, email):
        obj = re.search(r'[\w.]+\@[\w.]+', email)
        if not obj:
            raise ValidationError("Invalid Email")
