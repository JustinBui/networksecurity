
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load .env into environment variables
load_dotenv()

username = os.environ["MONGO_USERNAME"]
password = os.environ["MONGO_PASSWORD"]
uri = f"mongodb+srv://{username}:{quote_plus(password)}@cluster0.5gsacs2.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)