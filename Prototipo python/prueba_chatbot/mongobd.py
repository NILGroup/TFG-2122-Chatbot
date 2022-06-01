from pymongo import MongoClient
import json


def connection():
    client = MongoClient(port=27017)
    db = client.Ricorda
    return db



def query():
    db = connection()

    results = db.conversaciones.find()
    elements = []
    print("Holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    for result in results:
        elements.append(result['conversacion'])

    return elements
