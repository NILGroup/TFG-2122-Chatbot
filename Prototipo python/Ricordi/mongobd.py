from pymongo import MongoClient
import json

def connection():
    client = MongoClient(port=27017)
    db = client.Ricorda
    return db


def query():
    db = connection()

    result = db.preguntas.aggregate([{ "$sample": { "size": 1 } }])
    elements = []
    #i = 0
    #for result in results:
    result = list(result)
    res = result[0]
    elements.append(res["pregunta"])
    j = 2
    while "pregunta" + str(j) in res:
        elements.append(res["pregunta" + str(j)])
        j += 1

    return elements

def insert(question, answer):
    db = connection()

    doc = {"pregunta": question, "respuesta": answer}
    db.respuestas.insert_one(doc)
