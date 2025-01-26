from flask import request, jsonify, Blueprint, current_app
from marshmallow import ValidationError
from app.schemas.client_schema import DniSchema
from app.services import client_services
import app

client_bp = Blueprint('client', __name__)
dni_schema= DniSchema()


@client_bp.route('/clients/<dni>', methods=['GET'])
def get_client(dni):
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
def run_simulation(dni):
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
def create_client():
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
def update_client(dni):
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
def delete_client(dni):
  try:
    ret_data = client_services.delete_client(dni)
    if(ret_data.get('error')):
      return jsonify({"message": "Se ha producido un error. " + ret_data.get('error_msg')}), ret_data.get('error_code')
    else:
      return jsonify({'message': 'Cliente eliminado satisfactoriamente'})
  except Exception as err:
    current_app.logger.warning("Error create_client: " + str(err.args))
    return jsonify({"message": "Internal Server Error"}), 500