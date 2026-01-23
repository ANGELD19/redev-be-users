from marshmallow import Schema, fields, validate


class CreateUserSchema (Schema):
    first_name = fields.Str(required = True)
    middle_name = fields.Str(required = False)
    last_name = fields.Str(required = True)
    second_last_name = fields.Str(required = True)
    birthdate = fields.Date(required = True)
    type_of_plan = fields.Str(required = False)
    beneficiaries = fields.Str(required = True)
    email = fields.Str(required = True)
    phone = fields.Str(required = True)
    address = fields.Str(required = True)
    document_type = fields.Str(required = True, validate=validate.Regexp(r"^[A-Z]{2,3}$"))  # Ej: CC, TI, CE, PAS
    document = fields.Str(required = True)
    password = fields.Str(required = True)