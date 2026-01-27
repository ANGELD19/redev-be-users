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
    CreateUserSchema,UserEeditSchema 
    
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
            schema = CreateUserSchema()
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
            return handle_general_error(e, origen, 500) 
            

            if not user : 
                return handle_client_error("Usuario no encontrado", origen, 404)
            if not user.get("is_active", False):
                return handle_client_error("Usuario inactivo", origen, 404)
            if not bcrypt.check_password_hash(user.get("password"), data.get("password")):
                return handle_client_error("Contrasena incorrecta", origen, 401)
            
            token = create_access_token(
                identity = user.get("email"),
                expires_delta = datetime.timedelta(hours = 1) 
                )   
            user.pop("password", None)

            log_repository.create_log(origen, "ingreso correctamente", 200, user_id = user.get("_id"))
            response = {
                "data":{"token":token, "user":user},"message":"Ingreso correctamente"
            }
            return json.loads(json_util.dumps(response)), 200

        
          
        




      