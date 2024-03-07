from app.config.mysqlconnector import MySQLConnection
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:

    DB = "concert_hall_schema"

    def __init__(self, data):
        
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def register(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, username, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s)"""
        result = MySQLConnection(cls.DB).query_db(query, data)
        return result
    
    @classmethod
    def get_by_email(cls, email):
        query = """SELECT
        *
        FROM
        users
        WHERE
        email = %(email)s
        ;"""
        results = MySQLConnection(cls.DB).query_db(query, {"email": email})
        if results:
            return User(results[0])
        else:
            return False
        
    @classmethod
    def get_by_username(cls, username):
        query = """SELECT
        *
        FROM
        users
        WHERE
        username = %(username)s
        ;"""
        results = MySQLConnection(cls.DB).query_db(query, {"username": username})
        if results:
            return User(results[0])
        else:
            return False

    @classmethod
    def get_by_id(cls, id):
        query = """SELECT
        *
        FROM
        users
        WHERE
        id = %(id)s
        ;"""
        results = MySQLConnection(cls.DB).query_db(query, {"id": id})
        return User(results[0])

    @staticmethod
    def validate_new_user(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']):
            flash('invalid email format')
            is_valid = False
        elif User.get_by_email(data['email']):
            flash("Email already registered")
            is_valid = False
        if data['password'] != data["confirm_password"]:
            flash("passwords must match")
            is_valid = False
        if len(data['first_name']) < 3:
            flash("First name must be longer than 2 characters")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be longer than 2 characters")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be longer than 8 characters")
            is_valid = False
        if len(data['username']) < 3:
            flash("username must be longer than 2 characters")
            is_valid = False
        elif User.get_by_username(data['username']):
            flash("Username already registered")
            is_valid = False
        return is_valid