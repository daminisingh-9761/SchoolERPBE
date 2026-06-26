from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)

db = client["schoolERP"]

users_collection = db["users"]
students_collection = db["students"]
teachers_collection = db["teachers"]
attendance_collection = db["attendance"]
fees_collection = db["fees"]
fee_payments_collection = db["fee_payments"]


print("MongoDB Connected Successfully")