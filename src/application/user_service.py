import os
import json
import datetime
import string
import secrets
import traceback

from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from bson import ObjectId, json_util
from flask import jsonify, request, Flask
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token 

from src.infrastructure.repositories.mongodb.log_repository import LogRepository
from src.infrastructure.repositories.mongodb.user_repository import UserRepository
from src.domain.user_schema import (
    UserCreateSchema,UserEditSchema 
    
)

from src.infrastructure.utils.handler_error import (
    handle_general_error,
    handle_client_error
)

load_dotenv()
app = Flask (__name__)

bcrypt = Bcrypt()
log_repository = LogRepository()
user_repository = UserRepository()


class User:
    def __init__(self, app):      #Hace que las clases se inicien
        self.app = app              #(self) es un parametro obligatorio y es una referencia al objeto actual que se esta usando
                                    #app es la instacia de flask              
    def Create(self):
        origen = "Create User"            #origen =: nos va a indicar en caso de que se presente un error saber en que parte la presenta
        try: 
            data = request.get_json()
            schema = UserCreateSchema()
            schema.load(data)

            user = user_repository.create_user(data)
            user.pop("password", None)
            log_repository.create_log(origen, "exitoso", f"iser_id: {user['_id']}")

            response = {
                "message": "El ususario se ha creado exitosamente",
                "user": user
            }

            log_repository.create_log(origen, "exitoso", 200, user_id=user.get("_id")) 
            return json.loads(json_util.dumps(response)),200 #json_util.dumps(response) = convierte el diccionario response a JSON compatible con MongoDB
                                                             #json.loads = convierte ese JSON en un diccionario python estandar

        except ValidationError as e:
            return json.loads(json_util.dumps({
                "message": "Datos inválidos",
                "errors": e.messages
            })), 400
    
        except ValueError as e:
            return json.loads(json_util.dumps({
                "message": str(e)
            })), 400

        except Exception as e:
            return handle_general_error(e, origen) 
            
    def edit(self, user_id):
        origen = "Editar Usuario"
        try:                                 #todo lo que este adentro se intenta ejecutar y si falla algo -> se captura el error 
            data = request.get_json()        #lee el JSON enviado por el cliente 
            data["_id"] = user_id         
            schema = UserEditSchema()
            schema.load(data)

            updated_user = user_repository.edit_user(user_id, data)
            updated_user.pop ("password", None)
            log_repository.create_log(
                origen, "Exitoso", f"user_id: {user_id}"
            )

            response = {
                "message": "El usuario se ha editado con éxito",
                "user": data
            }

            return json.loads(json_util.dumps(response)), 200
        
        except ValueError as e:
            return jsonify({"message": str(e)}), 400
        except ValidationError as e:
            return jsonify({"message": "Datos inválidos", "errors": e.messages}), 400
        except Exception as e:
            return handle_general_error(traceback.format_exc(), origen)
          
        




      