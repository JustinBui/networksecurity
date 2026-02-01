import os
import sys
import json
from urllib.parse import quote_plus
import certifi
import pandas as pd
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from dotenv import load_dotenv

load_dotenv()

username = os.environ["MONGO_USERNAME"]
password = os.environ["MONGO_PASSWORD"]
MONGO_DB_URL = f"mongodb+srv://{username}:{quote_plus(password)}@cluster0.5gsacs2.mongodb.net/?appName=Cluster0"

print(MONGO_DB_URL)


# Making secure HTTP connection to MongoDB database 
ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    # Load environment variables from .env file
    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database 
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)

            return len(self.records)
        
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

if __name__ == "__main__":
    FILE_PATH = "Network_Data/phishingData.csv"
    DATABASE = "NetworkSecurityDB"
    Collection = "NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_converter(file_path=FILE_PATH)
    print(records)
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, Collection)
    print(no_of_records)