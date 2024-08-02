from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
from datetime import datetime

class Trips:
    db = "belt_exam_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.destination = data['destination']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.organizer = data['organizer']
        self.itinerary = data['itinerary']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
    
    #staticmethod for validating trip
    @staticmethod
    def validate(data):
        is_valid = True
        if len(data["destination"].strip()) == 0: 
            flash("*Must include a destination.")
            is_valid = False
        elif len(data["destination"].strip()) < 2: 
            flash("*Destination must be longer than three characters.")
            is_valid = False
        if len(data["start_date"].strip()) == 0: 
            flash("*Must include a start date.")
            is_valid = False
        else:
            now = datetime.now()
            trip_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
            if trip_date < now:
                is_valid = False
                flash("*Start date must be in the future.")
        if len(data["end_date"].strip()) == 0: 
            flash("*Must include an end date.")
            is_valid = False
        else:
            start = datetime.strptime(data["start_date"], "%Y-%m-%d")
            end = datetime.strptime(data["end_date"], "%Y-%m-%d")
            if end < start:
                is_valid = False
                flash("*End date must be later than start date.")
        if len(data["itinerary"].strip()) == 0: 
            flash("*Must include an itinerary.")
            is_valid = False
        elif len(data["itinerary"].strip()) > 50: 
            flash("*Itinerary must be less than 50 characters.")
            is_valid = False
        return is_valid

    #classmethod for save
    @classmethod
    def save(cls, data):
        query = """INSERT INTO trips (destination, start_date, end_date, organizer, itinerary, created_at)
                VALUES (%(destination)s, %(start_date)s, %(end_date)s, %(organizer)s, %(itinerary)s, NOW());"""
        return connectToMySQL(cls.db).query_db(query, data)
        
    #classmethod for update
    @classmethod
    def update(cls, data):
        query = """UPDATE trips
                SET destination=%(destination)s, start_date=%(start_date)s,
                    end_date=%(end_date)s, itinerary=%(itinerary)s, updated_at=NOW()
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query,data)
        
    #classmethod for delete
    @classmethod
    def delete(cls, id):
        query  = "DELETE FROM trips WHERE id = %(id)s;"
        data = {"id":id}
        return connectToMySQL(cls.db).query_db(query, data)

    #classmethod for getting all trips with users
    @classmethod
    def get_all_trips_with_users(cls):
        query = """SELECT * FROM trips
                JOIN booked_trips ON booked_trips.trip_id = trips.id 
                JOIN users ON booked_trips.user_id = users.id;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_trips = []
        for row in results:
            one_trip = cls(row)
            one_trips_author_info = {
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            author = user.Users(one_trips_author_info)
            one_trip.creator = author
            all_trips.append(one_trip)
        return all_trips
    
    #classmethod for base linking trips and users
    @classmethod
    def link(cls, data):
        query = """INSERT INTO booked_trips (user_id, trip_id)
                VALUES (%(user_id)s, %(trip_id)s);"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    #classmethod for deleting base link
    @classmethod
    def unlink(cls, id):
        query = """DELETE FROM booked_trips WHERE trip_id=%(id)s;"""
        data = {"id":id}
        return connectToMySQL(cls.db).query_db(query, data)
    
    #classmethod for getting one trip with user
    @classmethod
    def get_one_trip_with_users(cls, id):
        query = """SELECT * FROM trips
                JOIN booked_trips ON booked_trips.trip_id = trips.id 
                JOIN users ON booked_trips.user_id = users.id;"""
        data = {"id":id}
        results = connectToMySQL(cls.db).query_db(query, data)
        trip = Trips(results[0])
        user_data = {
            "id": results[0]['users.id'], 
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at']
                }
        trip.user = user.Users(user_data)
        return trip