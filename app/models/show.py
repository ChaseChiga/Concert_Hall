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

        if not results:
            return False
        show = cls(results[0])
        show.creator = User({
            "id": results[0]["users.id"],
            "first_name": results[0]["first_name"],
            "last_name": results[0]["last_name"],
            "username": results[0]["username"],
            "email": results[0]["email"],
            "password": results[0]["password"]
        })
        return show

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO shows (name, artist, location, date, rating, thoughts, public, user_id)
            VALUES (%(name)s, %(artists)s, %(location)s, %(date)s, %(rating)s, %(thoughts)s, %(public)s, %(user_id)s)"""
        result = MySQLConnection(cls.DB).query_db(query, data)
        print(result)
        return result

    @classmethod
    def edit(cls, data):
        query = """
            UPDATE shows
            SET
            name = %(name)s,
            artist = %(artists)s,
            location = %(location)s, 
            date = %(date)s, 
            rating = %(rating)s, 
            thoughts = %(thoughts)s,
            public = %(public)s
            WHERE id = %(id)s
            ;"""
        result = MySQLConnection(cls.DB).query_db(query, data)
        return result
    
    @classmethod
    def delete(cls,id):
        query = """ 
            DELETE
            FROM
                shows
            WHERE
                id = %(id)s
            ;
        """
        return MySQLConnection(cls.DB).query_db(query, {"id": id})
    
    @classmethod
    def get_all_but_user(cls, user_id):
        query = """SELECT *
        FROM
        shows
        JOIN
                users 
            ON 
                shows.user_id = users.id
        WHERE 
            shows.user_id != %(user_id)s
        and 
            shows.public = 1 
        ;"""
        results = MySQLConnection(cls.DB).query_db(query, {"user_id": user_id})
        print(f"!!!! {results} !!!!!!!!")
        all_results = []
        for row in results:
            show = cls(row)
            show.creator = User({
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "username": row["username"],
                "email": row["email"],
                "password": row["password"]
        })
            all_results.append(show)
        return all_results

    
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