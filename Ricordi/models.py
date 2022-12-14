from webbrowser import get
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
'''from run import mysql'''


'''def check_password(user, password):
    return check_password_hash(user[3], password)


def save_user(name, email, password):
    password = generate_password_hash(password)
    mysql.cursor.execute("INSERT INTO flask(name, email, password) VALUES (%s, %s, %s)",
                       (name, email, password))
    mysql.cursor.commit()


def get_user(email):
    mysql.cursor.execute("SELECT * FROM flask WHERE email = %s", email)
    user = mysql.cursor.fetchone()
    return user'''

import pymysql


def obtener_conexion():
    return pymysql.connect(host='localhost',user='root', password='tfg_2022',db='flask')

class User(UserMixin):

    def __init__(self, id, name, email, password, type):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.type = type


    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO users(name, email, password, type) VALUES (%s, %s, %s, %s)",
                       (self.name, self.email, self.password, self.type))
        conexion.commit()
        conexion.close()
        '''mysql.cursor().execute("INSERT INTO users(name, email, password) VALUES (%s, %s, %s)",
                       (self.name, self.email, self.password))
        mysql.commit()'''

    @staticmethod
    def get_by_id(id):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = '%s'", id)
            query = cursor.fetchone()
        conexion.close()
        if query is not None:
            user = User(query[0], query[1], query[2], query[3], query[4])
            return user
        else:
             return None

        '''mysql.cursor().execute("SELECT * FROM users WHERE id = %s", id)
        query = mysql.cursor().fetchone()
        user = User(query[0], query[1], query[2], query[3])'''
        return user

    @staticmethod
    def get_by_email(email):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", email)
            query = cursor.fetchone()
        conexion.close()
        if query is not None:
            user = User(query[0], query[1], query[2], query[3], query[4])
            return user
        else:
             return None

    @staticmethod
    def get_therapists_patients(id):
        conexion = obtener_conexion()
        patients = []
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM therapy WHERE therapist = %s", id)
            query = cursor.fetchall()
        conexion.close()
        for row in query:
            user = None
            if row[2] is not None:
                user = User.get_by_id(row[2])
            if user is not None:
                patients.append(user)
        return patients

    

class Therapy():
    def __init__(self, id, therapist, patient, code, user):
        self.id = id
        self.therapist = therapist
        self.patient = patient
        self.code = code
        self.user = user

    '''def save(self):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO therapy(therapist, patient) VALUES (%d, %d)",
                       (self.therapist, self.patient))
        conexion.commit()
        conexion.close()'''

    def save(self):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE therapy SET patient = %s, code = NULL, user = NULL WHERE code = %s",
                       (self.patient, self.code))
        conexion.commit()
        conexion.close()

    def create(self):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO therapy(therapist, code, user) VALUES (%s, %s, %s)",
                       (self.therapist, self.code, self.user))
        conexion.commit()
        conexion.close()

    @staticmethod
    def get_by_code(code):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM therapy WHERE code = %s", code)
            query = cursor.fetchone()
        conexion.close()
        if query is not None:
            therapy = Therapy(query[0], query[1], query[2], query[3], query[4])
            return therapy
        else:
             return None
    
    @staticmethod
    def comprobar_num(num):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM therapy WHERE code = %s", num)
            query = cursor.fetchone()
        conexion.close()
        if query is not None:
            return True
        else:
             return False
    
    @staticmethod
    def get_patients_id(id):
        result = []
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM therapy WHERE therapist = %s", id)
            query = cursor.fetchall()
        conexion.close()
        for row in query:
            if row[2] is not None:
                result.append(row[2])

        return result

    @staticmethod
    def get_unused_codes(id):
        result = []
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM therapy WHERE therapist = %s", id)
            query = cursor.fetchall()
        conexion.close()
        for row in query:
            if row[2] is None and row[3] is not None:
                therapy = Therapy(row[0], row[1], row[2], row[3], row[4])
                result.append(therapy)

        return result
