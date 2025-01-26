from marshmallow import Schema, fields, ValidationError, post_load
from flask import current_app

remainder_table = ['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K', 'E']

def validate_dni(dni):
  current_app.logger.debug('Validando DNI ' + dni)
  """ Validates if a DNI is well formatted"""
  
  """
  DNI algorith:
  Divide number part by 23 and get the remainder. Get the char which corresponds to that remainder.

  If NIF: first char gets subtituted by number (X->0, Y->1, Z->2)
  """
  is_valid_dni = False


  try:
    if(len(dni) != 9):
      raise("El DNI debe medir 9 caracteres")
    
    if(dni[8].isalpha() == False):
      raise("El DNI debe terminar en un numero")

    final_dni = dni

    #Check if NIF and transforms into DNI
    match dni[0].upper():
      case 'X':
        final_dni = '0' + final_dni[1:9]
      case 'Y':
        final_dni[0] = '1' + final_dni[1:9]
      case 'Z':
        final_dni[0] = '2' + final_dni[1:9]
    
    #Apply DNI algorithm
    current_app.logger.debug('Aplicando Algoritmo DNI ' + final_dni)
    current_app.logger.debug(int(dni[:8]))
    control_char = remainder_table[int(dni[:8]) % 23]
    is_valid_dni = control_char == dni[8].upper()
  except Exception as err:
    current_app.logger.debug('Error validando el DNI ' + dni)
    current_app.logger.debug(err.args)
    is_valid_dni = False

  current_app.logger.debug("Valid dni: " + str(is_valid_dni))
  return is_valid_dni


class DniSchema(Schema):
  dni = fields.Str(required=True, validate=validate_dni)

  @post_load
  def process_data(self, data, **kwargs):
    #Make sure final letter is in UpperCase
    data['dni'] = data['dni'][:8] + data['dni'][8].upper()
    return data


class ClientSchema(Schema):
  dni = fields.Str(required=True, validate=validate_dni)
  nombre = fields.Str(required=True)
  email = fields.Email(required=True)
  capital_solicitado = fields.Float(required=True)

  @post_load
  def process_data(self, data, **kwargs):
    #Make sure final letter is in UpperCase
    data['dni'] = data['dni'][:8] + data['dni'][8].upper()
    return data

class SimulationSchema(Schema):
  tae= fields.Float(required=True)
  plazo_amortizacion = fields.Float(required=True)

