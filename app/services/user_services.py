from app.models.client import User
from app.models import db
from app.schemas import user_schema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask import current_app
from flask_jwt_extended import (JWTManager, create_access_token, get_jwt_identity)
import math


def authenticate_user(data):
  """Check user credentials and return jwt Token"""
  try:
    current_app.logger.debug('Inside authenticate_user(): ' + str(data))
    #Validate data
    validated_data = user_schema.UserSchema().load(data)
    user = db.session.get(User, validated_data.get('usuario'))
    if(user is None or user.passwd != validated_data.get('contra')):
      current_app.logger.debug('No se ha encontrado el usuario')
      return {"error": True, "error_code": 401, "error_msg": "Combinación usuario y contraseña erróneos"}
    else:
      current_app.logger.debug('Usuario encontrado')
      #Do the jwt authentication
      access_token = create_access_token(identity=user.username)

      ret_data = {
        "token": access_token
      }
      return {"error": False, "response": ret_data}

  except ValidationError as val_err:
    current_app.logger.warning('Error validando datos entrada: ' + str(data))
    return {"error": True, "error_msg": "Error en los datos enviados", "error_code": 400}

