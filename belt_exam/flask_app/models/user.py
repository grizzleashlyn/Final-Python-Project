from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Users:
    db = "belt_exam_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #staticmethod for validating registration
    @staticmethod
    def validate_user(data):
        is_valid = True

        if len(data["first_name"].strip()) == 0: 
            flash("Please enter first name.", "register")
            is_valid = False
        elif len(data["first_name"].strip()) < 2: 
            flash("First name must be at least 2 characters.", "register")
            is_valid = False
        if len(data["last_name"].strip()) == 0: 
            flash("Please enter last name.", "register")
            is_valid = False
        elif len(data["last_name"].strip()) < 2: 
            flash("Last name must be at least 2 characters.", "register")
            is_valid = False
        if len(data["email"].strip()) == 0:
            flash("Please enter email.", "register")
            is_valid = False
        elif not EMAIL_REGEX.match(data["email"].strip()):
            flash("Invalid email address.", "register")
            is_valid = False
        if len(data["password"].strip()) == 0:
            flash("Please enter password.", "register")
            is_valid = False
        elif len(data["password"].strip()) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        elif data["password"] != data["confirm_password"]:
            flash("Passwords do not match.", "register")
            is_valid = False
        return is_valid

    #staticmethod for validating login
    @staticmethod
    def validate_login(data):
        is_valid = True
        if len(data["email"].strip()) == 0:
            flash("Please enter email.", "login")
            is_valid = False
        elif not EMAIL_REGEX.match(data["email"].strip()): 
            flash("Invalid email address.", "login")
            is_valid = False
        if len(data["password"].strip()) == 0:
            flash("Please enter password.", "login")
            is_valid = False
        elif len(data["password"].strip()) < 8:
            flash("Password must be at least 8 characters.", "login")
            is_valid = False
        return is_valid

    #classmethod for new user
    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"""
        user_id = connectToMySQL(cls.db).query_db(query,data)
        return user_id
    
    #classmethod for finding a user in the users table by id
    @classmethod
    def get_one_by_id(cls, id):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        data = {'id': id}
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return None
        return cls(results[0])
    
    #classmethod for finding a user in the users table by email
    @classmethod
    def get_one_by_email(cls, email):
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        data = {'email': email}
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return None
        return cls(results[0])