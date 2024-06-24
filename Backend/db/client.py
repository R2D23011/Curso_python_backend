from pymongo import MongoClient

#Base de Datos Remota
db_client = MongoClient(
    "mongodb+srv://carlitosaac16:ca27127850@clustermain.knks6a9.mongodb.net/?retryWrites=true&w=majority&appName=Clustermain").test


#Base de datos local
#db_client = MongoClient().local
