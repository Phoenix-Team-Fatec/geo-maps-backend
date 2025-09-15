from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME')


client = MongoClient(MONGO_URL)

db = client[DB_NAME]


if __name__ == "__main__":
    print("Conexão com o Mongo feita com sucesso")





