from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("MONGO_DATABASE_USERNAME").strip('"')
password = os.getenv("MONGO_DATABASE_PASSWORD").strip('"')
cluster = os.getenv("MONGO_DATABASE_CLUSTER").rstrip("/")

MONGO_URI = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority"

if os.getenv("FLASK_ENV") == "development":
    print("MONGO_URI:", MONGO_URI)

client = MongoClient(MONGO_URI, maxPoolSize=100)

def get_mongo_client():
    user = os.getenv("MONGO_DATABASE_USERNAME")
    password = os.getenv("MONGO_DATABASE_PASSWORD")
    cluster = os.getenv("MONGO_DATABASE_CLUSTER")
    uri = f"mongodb+srv://{user}:{password}@{cluster}/"
    return MongoClient(uri)



