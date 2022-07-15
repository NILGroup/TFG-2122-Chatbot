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

    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password


    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO users(name, email, password) VALUES (%s, %s, %s)",
                       (self.name, self.email, self.password))
        conexion.commit()
        conexion.close()
        '''mysql.cursor().execute("INSERT INTO users(name, email, password) VALUES (%s, %s, %s)",
                       (self.name, self.email, self.password))
        mysql.commit()'''

    @staticmethod
    def get_by_id(id):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", id)
            query = cursor.fetchone()
        conexion.close()
        if query is not None:
            user = User(query[0], query[1], query[2], query[3])
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
            user = User(query[0], query[1], query[2], query[3])
            return user
        else:
             return None

        '''mysql.cursor().execute("SELECT * FROM users WHERE email = %s", email)
        query = mysql.cursor().fetchone()
        user = User(query[0], query[1], query[2], query[3])'''