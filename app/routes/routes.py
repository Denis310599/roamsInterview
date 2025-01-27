from flask import request, jsonify, Blueprint, current_app
from marshmallow import ValidationError
from app.schemas.client_schema import DniSchema
from app.services import client_services, user_services
import app
from flask_jwt_extended import (get_jwt_identity, jwt_required)

client_bp = Blueprint('client', __name__)
dni_schema= DniSchema()

#************************************************
#************ Client Related Functions  *********
#************************************************
@client_bp.route('/clients/<dni>', methods=['GET'])
@jwt_required()
def get_client(dni):
  """Gets the client based on a DNI, if exists. Returns the client"""
  try:
    ret_data = client_services.get_client(dni)
    if(ret_data.get('error')):
      current_app.logger.debug("Error al realizar get_clients()")
      return jsonify({"message": "Se ha producido un error. " + ret_data.get('error_msg')}), ret_data.get('error_code')
    else:
      current_app.logger.debug("Datos consultados")
      return jsonify(ret_data.get('response'))
  except Exception as err:
    current_app.logger.warning("Error getClients: " + str(err.args))
    return jsonify({"message": "Internal Server Error"}), 500

@client_bp.route('/clients/<dni>', methods=['POST'])
@jwt_required()
def run_simulation(dni):
  """Runs a new simulation based on a client and some input data, returns the result and stores it in the database"""
  try:
    body_data = request.get_json()
    ret_data = client_services.run_simulation(dni, body_data)

    if(ret_data.get('error')):
      current_app.logger.debug("Error al realizar run_simulation()")
      return jsonify({"message": "Se ha producido un error. " + ret_data.get('error_msg')}), ret_data.get('error_code')
    else:
      current_app.logger.debug("Datos consultados")
      return jsonify(ret_data.get('response'))
  except Exception as err:
    current_app.logger.warning("Error run_simulation: " + str(err.args))
    return jsonify({"message": "Internal Server Error"}), 500



@client_bp.route('/clients', methods=['POST'])
@jwt_required()
def create_client():
  """Creates a new client if it doesn't exist"""
  try:
    data = request.get_json()
    current_app.logger.info("Data: " + str(data))
    ret_data = client_services.create_client(data)
    if(ret_data.get('error')):
      return jsonify({"message": "Se ha producido un error. " + ret_data.get('error_msg')}), ret_data.get('error_code')
    else:
      return jsonify({'message': 'Cliente creado satisfactoriamente'})
  except Exception as err:
    current_app.logger.warning("Error create_client: " + str(err.args))
    return jsonify({"message": "Internal Server Error"}), 500


@client_bp.route('/clients/<dni>', methods=['PATCH'])
@jwt_required()
def update_client(dni):
  """Updates the data of a client if it exists"""
  try:
    data = request.get_json()
    current_app.logger.info("Data: " + str(data))
    ret_data = client_services.update_client(data, dni)
    if(ret_data.get('error')):
      return jsonify({"message": "Se ha producido un error. " + ret_data.get('error_msg')}), ret_data.get('error_code')
    else:
      return jsonify({'message': 'Cliente actualizado satisfactoriamente'})
  except Exception as err:
    current_app.logger.warning("Error create_client: " + str(err.args))
    return jsonify({"message": "Internal Server Error"}), 500


@client_bp.route('/clients/<dni>', methods=['DELETE'])
@jwt_required()
def delete_client(dni):
  """Deletes a client that has this DNI"""
  try:
    ret_data = client_services.delete_client(dni)
    if(ret_data.get('error')):
      return jsonify({"message": "Se ha producido un error. " + ret_data.get('error_msg')}), ret_data.get('error_code')
    else:
      return jsonify({'message': 'Cliente eliminado satisfactoriamente'})
  except Exception as err:
    current_app.logger.warning("Error create_client: " + str(err.args))
    return jsonify({"message": "Internal Server Error"}), 500


#************************************************
#*********** Users related functions    *********
#************************************************
user_bp = Blueprint('auth', __name__)

@user_bp.route('/user/login', methods=['POST'])
def login():
  """Returns a jwt token for accessing the API"""
  try:
    data = request.get_json()
    ret_data = user_services.authenticate_user(data)
    if(ret_data.get('error')):
      current_app.logger.debug("Error al realizar login()")
      return jsonify({"message": "Se ha producido un error. " + ret_data.get('error_msg')}), ret_data.get('error_code')
    else:
      current_app.logger.debug("Login correcto")
      return jsonify(ret_data.get('response'))
  except Exception as err:
      current_app.logger.warning("Error getClients: " + str(err.args))
      return jsonify({"message": "Internal Server Error"}), 500