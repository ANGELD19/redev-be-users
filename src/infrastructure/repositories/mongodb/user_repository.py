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




































    def get_users(self, page, page_size, filters):
        #Filtro por defecto: solo activos si no se especifica
        if "is_active" not in filters:
            filters["is_active"] = True
        else:
            if isinstance(filters["is_active"], str):
               #isintance sirve para preguntar que valor es:¿El valor de is_active es un texto (string)?
                filters["is_active"] = filters["is_active"].lower() == "true"

        search_term = filters.pop("search", None)
        #Sirve para guardar el texto que el usuario quiere buscar
        query = dict(filters)
        #Esto crea una copia del diccionario filters
        #Que hace dict(filters) = Crea otro diccionario nuevo con el mismo contenido 
        #query es el diccionario que se va a suar para consultar la base de datos
        query = dict(filters)

        if search_term:
            query = {
                "$and": [     #Sirve para decirle a MongoDB:"Cumple todas estas condiciones al mismo tiempo"
                    query,
                    {
                        "$or": [    #Es un operador de MongoDB y significa "O"logico, se usa cuando basta con que se cumpla una condicion, no todas 
                            {"first_name": {"$regex":search_term, "$options": "i"}},   #Buscar usuarios cuyo first_name contenga el texto que escribió el usuario sin importar mayúsculas o minúsculas
                            {"middle_name": {"$regex":search_term, "$options": "i"}},  #"$regex" = permite buscar texto parcial
                            {"last_name": {"$regex":search_term, "$options": "i"}},    #La [i] = significa ignorar mayuscula y minusculas
                            {"second_last_name": {"$regex":search_term, "$options": "i"}},                       
                        ]
                    }
                ]    
            }

        return self.get_all(  #get_all Hace:consulta a MongoDB, Aplica filtros, Aplica paginacion, Devuelve datos
            page=page,
            page_size=page_size,
            details=self.add_details(),
            **query
        )
    

    def get_user(self, _id):
        return self.get(
            details=self.add_details(),
            _id=ObjectId(_id))
        