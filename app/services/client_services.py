from app.models.client import Client, Simulation
from app.models import db
from app.schemas import client_schema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask import current_app
import math
def create_client(data):
  """Creates a new client"""
  try:
    current_app.logger.debug('Inside create_client(): ' + str(data))
    #Validates data
    validated_data = client_schema.ClientSchema().load(data)
    client = Client(
      dni = validated_data.get('dni'),
      nombre = validated_data.get('nombre'),
      email = validated_data.get('email'),
      capital_solicitado = validated_data.get('capital_solicitado')
    )
    db.session.add(client)
    db.session.commit()
  except ValidationError as val_err:
    current_app.logger.warning('Data Validation Error. ' + str(val_err))
    return {"error": True, "error_code": 400, "error_msg": "Los datos enviados son erroneos"}
  except IntegrityError as errInt:
    return {"error": True, "error_code": 200, "error_msg": "Ya existe registrado con el mismo DNI"}
  
  return {"error": False, "response": None}


def get_client(data):
  """Get a specific stored client, based on it's DNI"""
  try:
    current_app.logger.debug('Inside GetClient(): DNI - ' + data)
    #Validate data
    validated_data = client_schema.DniSchema().load({"dni": data})
    client = db.session.get(Client, validated_data.get('dni'))
    if(client is None):
      current_app.logger.debug('No se ha encontrado el cliente')
      return {"error": True, "error_code": 404, "error_msg": "No se ha encontrado ningun cliente con los datos introducidos"}
    else:
      current_app.logger.debug('Cliente encontrado')
      ret_data = {
        "dni": client.dni,
        "nombre": client.nombre,
        "email": client.email,
        "capital_solicitado": client.capital_solicitado
      }
      return {"error": False, "response": ret_data}

  except ValidationError as val_err:
    current_app.logger.warning('Error validando datos entrada: ' + data)
    return {"error": True, "error_msg": "Error en los datos enviados. " + str(val_err), "error_code": 400}
  
def run_simulation(dni, data): 
  """Calculates a simulation for a given client and stores the result in the dataBase"""
  try:
    current_app.logger.debug('Inside run_simulation(): dni - ' + str(dni) + ". Data: " + str(data))
    validated_dni = client_schema.DniSchema().load({"dni": dni})
    validated_sim_data = client_schema.SimulationSchema().load(data)

    #Retreives the client data
    client = db.session.get(Client, validated_dni)
    if(client is None):
      current_app.logger.debug('No se ha encontrado el cliente')
      return {"error": True, "error_code": 404, "error_msg": "No se ha encontrado ningun cliente con los datos introducidos"}

    #Calculates the simulation
    calculated_simulation = calculate_simulation(client.capital_solicitado, validated_sim_data.get('tae'), validated_sim_data.get('plazo_amortizacion'), validated_dni.get('dni')) 
  
    #Adds this sim to the DB
    current_app.logger.debug("Guardando simulación " + str(calculated_simulation))
    db.session.add(calculated_simulation)
    db.session.commit()

    #returns the data
    return {"error": False, "response": {"cuota_mensual": calculated_simulation.cuota_mensual,
                                         "importe_devolver": calculated_simulation.importe_devolver}}

  except ValidationError as val_err:
    current_app.logger.warning('Error validando datos entrada: ' + data)
    return {"error": True, "error_msg": "Error en los datos enviados. " + str(val_err), "error_code": 400}

def calculate_simulation(capital, tae, plazo_amortizacion, dni):
    current_app.logger.debug("calculate_simulation(). Capital: " + str(capital) + ", tae: " + str(tae) + ", plazo amortizacion: " + str(plazo_amortizacion))
    try:
      """
      Runs the simulation
        cuota = capital * i / (1-(1+i)^(-n))

        capital: prestamo hipotecario
        i: tipo de interes (Tae/100/12)
        n: meses de plazo amortizacion
      """
      tipo_interes = tae/(100*12)
      meses_amortizacion = plazo_amortizacion*12
      cuota = capital * tipo_interes / (1- math.pow(1+tipo_interes, -1*meses_amortizacion))
      cuota = round(cuota, 2)

      importe_total = cuota*meses_amortizacion
      current_app.logger.debug('Cuota calculada: ' + str(cuota) + '. Importe total: ' + str(importe_total))

      new_simulation = Simulation(
        dni = dni,
        capital = capital,
        tae = tae,
        plazo_amortizacion = plazo_amortizacion,
        cuota_mensual = cuota,
        importe_devolver = importe_total
      )
    except ZeroDivisionError as err:
      current_app.logger.warning("Error al calcular la simulacion. Division entre 0")
      raise("Error al calcular la cuota, resltado negativo")
    except Exception as err2:
      current_app.logger.warning("Error al calcular la simulacion. " + str(err2));
      raise("Error al calcular la cuota. " + str(err2)) 

    return new_simulation
    
  
def update_client(data, dni):
  """Creates a new client"""
  try:
    complete_data = data
    complete_data["dni"] = dni
    current_app.logger.debug('Inside update_client(): ' + str(complete_data))
     
    #Validates data
    validated_data = client_schema.ClientSchema().load(complete_data)

    #Check client exists
    client = db.session.get(Client, {"dni": complete_data.get('dni')})
    if(client is None):
      return {"error": True, "error_code": 404, "error_msg": "No se ha encontrado ningun cliente con los datos introducidos"}

    #Update the object
    client.email = validated_data.get('email')
    client.nombre = validated_data.get('nombre')
    client.capital_solicitado = validated_data.get('capital_solicitado')

    #db.session.add(client)
    db.session.commit()
  except ValidationError as val_err:
    current_app.logger.warning('Data Validation Error. ' + str(val_err))
    return {"error": True, "error_code": 400, "error_msg": "Los datos enviados son erroneos"}
  
  return {"error": False, "response": None}

def delete_client(data):
  try:
    current_app.logger.debug('Inside DeleteClient(): DNI - ' + data)
    #Validate data
    validated_data = client_schema.DniSchema().load({"dni": data})
    client = db.session.get(Client, data)
    if(client is None):
      current_app.logger.debug('No se ha encontrado el cliente')
      return {"error": True, "error_code": 404, "error_msg": "No se ha encontrado ningun cliente con los datos introducidos"}
    else:
      current_app.logger.debug('Cliente Eliminado correctamente')
      db.session.delete(client) 
      db.session.commit()
      return {"error": False}

  except ValidationError as val_err:
    current_app.logger.warning('Error validando datos entrada: ' + data)
    return {"error": True, "error_msg": "Error en los datos enviados. " + str(val_err), "error_code": 400}

