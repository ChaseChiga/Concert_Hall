from app.config.mysqlconnector import MySQLConnection
from flask import flash
from datetime import date, datetime
from app.models.user import User

current_date =datetime.now()

class Show:

    DB = "concert_hall_schema"

    def __init__(self, data):
        
        self.id = data['id']
        self.name = data['name']
        self.artists = data['artist']
        self.location = data['location']
        self.date = data['date']
        self.rating = data['rating']
        self.thoughts = data['thoughts']
        self.user_id = data["user_id"]
        self.public = data['public']
        self.creator = None

    @classmethod
    def get_by_creator(cls, user_id):
        query = """SELECT *
        FROM
        shows
        WHERE shows.user_id = %(user_id)s
        ;"""
        results = MySQLConnection(cls.DB).query_db(query, {"user_id": user_id})
        return results

    @classmethod
    def get_by_id_with_creator(cls, id):
        query = """SELECT *
        FROM
        shows
        JOIN
        users 
        ON 
        shows.user_id = users.id
        WHERE shows.id = %(id)s
        ;"""
        results = MySQLConnection(cls.DB).query_db(query, {"id": id})
        return results[0]
    
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO shows (name, artist, location, date, rating, thoughts, public, user_id)
            VALUES (%(name)s, %(artists)s, %(location)s, %(date)s, %(rating)s, %(thoughts)s, %(public)s, %(user_id)s)"""
        result = MySQLConnection(cls.DB).query_db(query, data)
        print(result)
        return result

    @staticmethod
    def validate_new_show(data):
        is_valid = True
        if len(data['location']) < 1:
            flash("Location must not be blank")
            is_valid = False
        if len(data['thoughts']) < 1:
            flash("Your thoughts must not be blank")
            is_valid = False
        if len(data['date']) < 1:
            flash("The date of the show must not be blank")
            is_valid = False
        elif datetime.strptime(data['date'], '%Y-%m-%d') > current_date:
            flash("the Date of the show must be in the past")
            is_valid = False
        if len(data['name']) < 1:
            flash("The name of the show must not be blank")
            is_valid = False
        if len(data['artists']) < 1:
            flash("The show must have artists")
            is_valid = False
        if 'public' not in data:
            flash("you must select if the post is public or not")
            is_valid = False
        if len(data['rating']) < 1:
            flash("you must rate the show between 0 and 10")
            is_valid = False
        return is_valid