from marshmallow import Schema, fields, validate

from src.domain.general_validations import validate_hexadecimal


class UserCreateSchema (Schema):
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
    document_type = fields.Str(required = True)  # Ej: CC, TI, CE, PAS
    document = fields.Str(required = True, error="Document must be between 6 and 10 digits.")
    password = fields.Str(required = True)

class UserEditSchema (Schema):
    _id = fields.Str(required = True, validate=validate_hexadecimal)
    first_name = fields.Str(required = True)
    middle_name = fields.Str(required = False, allow_none=True)
    last_name = fields.Str(required = True)
    second_last_name = fields.Str(required = False, allow_none=True)
    birthdate = fields.Date(required = True)
    type_of_plan = fields.Str(required = False)
    beneficiaries = fields.Str(required = False, allow_none=True)
    email = fields.Email(required = True)
    phone = fields.Str(required = False, allow_none=True)
    address = fields.Str(required=False, allow_none=True)
    document_type = fields.Str(required = True, validate=validate.Regexp(r"^[A-Z]{2,3}$", error="Document must be between 6 and 10 digits."))  # Ej: CC, TI, CE, PAS
    document = fields.Str(required = True)
    password = fields.Str(required = False, allow_none=True)    