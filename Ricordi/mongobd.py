from pymongo import MongoClient
import json
import analyze_answer
import classify_answer
import text_analysis

def connection():
    client = MongoClient(port=27017)
    db = client.Ricorda
    return db

def asked_question(question, user_id):
    db = connection()
    asked = list(db.respuestas.find({"user_id": user_id,"pregunta": question}))
    #print(asked)
    return asked


def one_random_question(user_id):
    db = connection()

    result = db.preguntas.aggregate([{ "$sample": { "size": 1 } }])
    
    #i = 0
    #for result in results:
    result = list(result)
    res = result[0]
    question = res['pregunta']
    while asked_question(question, user_id):
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

def every_unasked_question(user_id):
    db = connection()

    results = db.preguntas.find()
    elements = []
    for result in results:
        question = result['pregunta']
        if not asked_question(question, user_id):
            elements.append(question)

    return elements

def insert_answer(question, answer, user_id):
    db = connection()

    categories = analyze_answer.clasificar_emocion(answer)
    categories += classify_answer.clasificar_etapas(answer)
    categories += text_analysis.analyze(answer)

    doc = {"user_id": user_id,"pregunta": question, "respuesta": answer, "categorias": categories}
    db.respuestas.insert_one(doc)
    #db.preguntas.update_one({"pregunta": question}, {"$set":{"asked": "True"}})

#insert_answer("hola", "Me llamo Lucía y tengo 23 años")

def get_patients_info(user):
    db = connection()
    answers = list(db.respuestas.find({"user_id": user}))
    return answers