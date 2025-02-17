from marshmallow import Schema, fields, ValidationError, post_load
from flask import current_app

class UserSchema(Schema):
  usuario = fields.Str(required=True)
  contra = fields.Str(required=True)

  @post_load
  def process_data(self, data, **kwargs):
    #Make sure username is in LowerCase
    data['usuario'] = data['usuario'].lower()
    return data
