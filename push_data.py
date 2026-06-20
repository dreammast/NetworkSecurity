import os
import sys
import json
import certifi 
import pandas as pd
import numpy as np
import pymongo
from pymongo import database
from network_security.exception.exception import NetworkSecurityException
from network_security.logging import logger

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ca = certifi.where()


class NetworkDataExtract():

    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_converter(self,file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True,inplace =True)
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__ == "__main__":
    FILE_PATH ="Network_data\phisingData.csv"
    database = "Nale"
    collection = "NetworkData"
    networkobj = NetworkDataExtract()
    records=networkobj.csv_to_json_converter(FILE_PATH)
    print(records)
    no_of_records = networkobj.insert_data_mongodb(records,database,collection)
    print(no_of_records)