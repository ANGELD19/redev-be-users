import os
import datetime

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import jwt_required, JWTManager     #@jwt_required = Es un decorador de seguridad que obliga a que la peticion tenga un JWT valido, si no hay token 
                                                            #o es invalido -> no entra a la funcion 
                                                            #Internamente busca el JWT en el header Authorization y verifica que el token exista, no este vencido y este bien firmado
from src.application.user_service import User
from src.middleware.hasRole import has_role #Esto significa que importa una funcion (o decorador) llamada has_role que se usa para controlar permisos/roles
#haas_role restringe el acceso a una ruta segun el rol usuario

##@has_role("admin")
#def edit_user():          Esto significa que solo usuarios con rol admin pueden entrar aqui 

app = Flask(__name__)
app.config["CHARSET"] = "UTF-8"
configurations = os.environ

app.config["JWT_SECRET_KEY"] = configurations.get("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=6)

jwt = JWTManager(app)

user = User(app)

CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "True"}})

@app.route("/")     #Se esta decorando indicando que dentro de la aplicacion va a estar ligada a la ruta raiz de la app        
def index():        #linea 26/27 crea una vista que se expresa en forma de funcion 
    return "Testing, Flask!"


#@app.route("/users", methods=["GET"])
#def get_users():
#    return user.get_all()

@app.route("/users/create-user", methods=["POST"])
@jwt_required()
#@has_role(["Admin", "SuperAdmin"])
def create_user():
    return user.Create()

@app.route("/users/edit-user/<user_id>", methods=["PUT"])
@jwt_required()
#@has_role(["Admin", "superAdmin"])
def edit_user(user_id):
    return user.edit(user_id)


if __name__ == '__main__':     #__main__ es el nombre del archivo principal que se ejecuta, Este EJECUTA el servidor SOLO si este archivo es el principal para eso es el IF 
    app.run(debug=True,port=6000)   #Esto ubica un puerto para que se abra directamente 


#<user_id>