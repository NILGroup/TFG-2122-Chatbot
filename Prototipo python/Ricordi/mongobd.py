from pymongo import MongoClient
import json

def connection():
    client = MongoClient(port=27017)
    db = client.Ricorda
    return db

def asked_question(question):
    db = connection()
    asked = list(db.respuestas.find({"pregunta": question}))
    #print(asked)
    return asked


def one_random_question():
    db = connection()

    result = db.preguntas.aggregate([{ "$sample": { "size": 1 } }])
    
    #i = 0
    #for result in results:
    result = list(result)
    res = result[0]
    question = res['pregunta']
    while asked_question(question):
        result = db.preguntas.aggregate([{ "$sample": { "size": 1 } }])
        result = list(result)
        res = result[0]
        question = res['pregunta']

    '''elements = []
    elements.append(question)
    j = 2
    while "pregunta" + str(j) in res:
        elements.append(res["pregunta" + str(j)])
        j += 1'''

    return question

def every_unasked_question():
    db = connection()

    results = db.preguntas.find()
    elements = []
    for result in results:
        question = result['pregunta']
        if not asked_question(question):
            elements.append(question)

    return elements

def insert_answer(question, answer):
    db = connection()

    doc = {"pregunta": question, "respuesta": answer}
    db.respuestas.insert_one(doc)
    #db.preguntas.update_one({"pregunta": question}, {"$set":{"asked": "True"}})

