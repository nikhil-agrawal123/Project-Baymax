from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")

uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@storage.9suwx.mongodb.net/?retryWrites=true&w=majority&appName=Storage"

client = MongoClient(uri, server_api=ServerApi('1'))

def has_id(id,name,age,gender,symptoms,duration,severity):
    db = client.test
    patients = db.Patients

    try:
        patients.insert_one({
            "_id": ObjectId(id),
            "name":name,
            "age":age,"gender":gender,
            "problem":symptoms,
            "duration": duration,
            "severity": severity,
            "time-stamp": f"{datetime.date.today()}",
            "doctor-remarks": "to be entered"
        })
        print("success")
    except Exception as e:
        print(e)

def new_id(name,age,gender,symptoms,duration,severity):
    db = client.test
    patients = db.Patients

    try:
        patients.insert_one({
            "name": name,
            "age": age, "gender": gender,
            "problem": symptoms,
            "duration": duration,
            "severity": severity,
            "time-stamp": f"{datetime.date.today()}",
            "doctor-remarks": "to be entered"
        })
        new_uuid = patients.inserted_id
        print(f"Your user id if: {new_uuid} please save it for future reference")
        print("success")
    except Exception as e:
        print(e)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)