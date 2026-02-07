
import os
import pandas as pd
import numpy as np
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from dotenv import load_dotenv
from networksecurity.constant import training_pipeline
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

    # Check if DB exists
    db_name = training_pipeline.DATA_INGESTION_DATABASE_NAME
    db_exists = False
    if db_name in client.list_database_names():
        print(f"Database '{db_name}' exists.")
        db_exists = True
    else:
        print(f"Database '{db_name}' does not exist.")

    # Check if collection exists
    collection_exists = False
    if db_exists:
        collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        db = client[db_name]
        if collection_name in db.list_collection_names():
            print(f"Collection '{collection_name}' exists in database '{db_name}'.")
            collection_exists = True
        else:
            print(f"Collection '{collection_name}' does not exist in database '{db_name}'.")
    
    if collection_exists:
        collection = db[collection_name]
        document_count = collection.count_documents({})
        print(f"Number of documents in collection '{collection_name}': {document_count}")


    df = pd.DataFrame(list(collection.find()))
    

    if "_id" in df.columns.to_list():
        df=df.drop(columns=["_id"],axis=1)
    df.replace({'na': np.nan}, inplace=True)
    
    print(df.head())
except Exception as e:
    print(e)