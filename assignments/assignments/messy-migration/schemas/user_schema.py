from marshmallow import Schema, fields, validate

class UserCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))

class UserUpdateSchema(Schema):
    name = fields.Str()
    email = fields.Email()

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
