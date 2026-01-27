import os
import bcrypt
import datetime
import json 
from src.domain.constant import SORT, LOOKUP
from bson import ObjectId
from src.infrastructure.repositories.mongodb.mongodb_repository import MongodbRepository

COLLECTION_NAME = "users"

class UserRepository(MongodbRepository):
    def __init__(self):
        user = os.getenv("MONGO_DATABASE_USERNAME")
        password = os.getenv("MONGO_DATABASE_PASSWORD")
        cluster = os.getenv("MONGO_DATABASE_CLUSTER")
        string_connection = f"mongodb+srv://{user}:{password}@{cluster}/"
        super().__init__(
            string_connection,
            os.getenv("MONGO_DATABASE_NAME"),
            COLLECTION_NAME,
        )

    def create_user(self, data ):         #def= define una funcion, #create_user = nombre de la funcion, #self= la clase misma, #data= informacion del usuario
        self.is_duplicated(email=data["email"])   #self.is_duplicated(email=data["email"]) = llama a una funcion llamada is_duplicated que revisa si ya existe un usuario con ese email 
        self.is_duplicated(document=data["document"]) #Hace lo mismo de revisar si existe y si ya existe esa funcion lanza un error

        today = datetime.datetime.now(datetime.timezone.utc)  #En general: obtiene la fecha y hora actual, en formato UTC, y la guarda en la variable today
        #variable - today,  #datetime.datetime = es una clase,  #datetime.datetime.now() = devuelve la fecha y la hora actuales,  #datetime.timezone.utc = esto indica la zona horaria

        plain_password = data.get("document")   #plain_password= es la contraseña en texto plan, tal como la escribe el usuario 
        #plain = sin proteccion,   
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()) #convierte una contrasena normal (texto) en un valor seguro (hash)
        #hashed = contraseña protegida, #bcrypt.hashpw = es una funcion de seguridad para cambiar las contrasenas normales en seguras 
        #bcrypt.gensalt() = es una funcion que genera un "salt" aleatorio que se usa para proteger la contrasena hace que cada una sea unica y segura
        #plain_password.encode('utf-8') = #code = convierte texto (str) en bytes porque bcrypt solo trabaja con bytes
        data = {
            
            "document_type": ObjectId(data.get("document_type")),
            "document": data.get("document"),
            
            "first_name": data.get("first_name"),
            "middle_name": data.get("middle_name", ""),
            "last_name": data.get("last_name"),
            "second_last_name": data.get("second_last_name", ""),
            
            "plan": [data.get("plan")],
            "process_types": [ObjectId(pt) for pt in data.get("process_types", [])],   #for pt in = es un bucle for: para cada elemento dentro de esa lista 
            #pt = es una variable temporal 
            #pt al inicio = esto indica que valor se va a guardar en la nueva lista
            "phone": data.get("phone", None),

            "email": data.get("email"),
            "password": hashed_password.decode('utf-8'),

            "created_at": today,
            "updated_at": today,
            "is_active": True,
        }
        
        response = self.create(**data)   #esto llama a una funcion create del repository    #(**data) = significa descomponer el diccionario y pasa cada clave como argumento
        _id = response.inserted_id  #inserted_id = es el ID que mongoDBle asigno al documento recien creado    #_id = se necesita para consultar el usuario recien creado
        return self.get(_id=ObjectId(_id)) #busca el documento recien creado en la base de datos y lo devuelve completo 

    def edit_user(self, user_id, data):
        #Obtener usuario actual
        existing_user = self.get(_id=ObjectId(user_id))
        if not existing_user:
            raise ValueError("Usuario no encontrado") #raise es fundamental para entender cómo Python maneja errores.
        
        self.is_duplicated(user_id=user_id, email=data.get("email", existing_user.get("email")))
        self.is_duplicated(user_id=user_id, document=data.get("document", existing_user.get("document")))


        updated_user = {
            "document_type": ObjectId(data.get("document_type")) if data.get("document_type") else existing_user["document_type"],
            "document": data.get("document", existing_user["document"]),

            "first_name": data.get("first_name", existing_user["first_name"]),
            "middle_name": data.get("middle_name",existing_user.get("middle_name", "")),
            "last_name": data.get("last_name", existing_user["last_name"]),
            "second_last_name": data.get("last_name", existing_user.get("second_last_name", "")),

            "password": existing_user["password"],
            "cellphone": data.get("cellphone", existing_user.get("cellphone")),
            "email": data.get("email", existing_user["email"]),
            "address": data.get("address", existing_user["address"]),
            "is_active": data.get("is_active", existing_user.get("is_active", True)),
            "updated_at": datetime.datetime.now(),
        }
        #Upgrade
        self.update(id=ObjectId(user_id), **updated_user) #Esta linea actualiza el usuario en la base de datos
        #self.update = un metodo de repository, ejecuta un update en MongoDB
        #id=ObjectId(user_id) = indica que usuario actualizar, user_id llega como string Mongo necesita ObjectId por eso se convierte
        #**updated_user = Expande el diccionario updated_user en argumentos
        return self.get(_id=ObjectId(user_id))
    
    