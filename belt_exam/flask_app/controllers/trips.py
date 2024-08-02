from flask_app import app, bcrypt
from flask_app.models.user import Users
from flask_app.models.trip import Trips
from flask import render_template, redirect, request, session, flash

#route for displaying index
@app.route('/')
def index():
    return render_template('index.html')

#route for processing registration
@app.post('/create_user')
def create():
    if not Users.validate_user(request.form):
            return redirect('/')
    
    potential_user = Users.get_one_by_email(request.form["email"])
    if potential_user != None:
        flash("Account already exists with this email. Please log in.", "register")
        return redirect ('/')
    
    hashed_password = bcrypt.generate_password_hash(request.form["password"])
    
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashed_password
    }
    user_id = Users.save(data)
    session["user_id"] = user_id
    return redirect('/trips')

#route for processing login
@app.post('/login')
def login():
    if not Users.validate_login(request.form):
            return redirect('/')
    potential_user = Users.get_one_by_email(request.form["email"])
    if potential_user == None:
        flash("Invalid login information.", "login")
        return redirect ('/')
    
    user = potential_user
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid login information.", "login")
        return redirect ('/')

    session["user_id"] = user.id
    return redirect('/dashboard')

#route for logging out
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#route for route for displaying dashboard
@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect('/')
    user=Users.get_one_by_id(session["user_id"])
    trips = Trips.get_all_trips_with_users()
    return render_template('dashboard.html', user=user, all_trips=trips)

#route for creating new trip
@app.route('/trips/new')
def createtrip():
    user=Users.get_one_by_id(session["user_id"])
    if "user_id" not in session:
        return redirect('/')
    return render_template("create.html", user=user)

#route for processing new trip
@app.post('/process')
def processtrip():
    if not Trips.validate(request.form):
            return redirect('/trips/new')
    trip_id = Trips.save(request.form)
    data = {
        "trip_id" : trip_id,
        "user_id" : session["user_id"]
    }
    Trips.link(data)
    return redirect('/dashboard')

#route for updating trip
@app.route('/trips/edit/<int:id>')
def edittrip(id):
    user=Users.get_one_by_id(session["user_id"])
    if "user_id" not in session:
        return redirect('/')
    trip = Trips.get_one_trip_with_users(id)
    return render_template('edit.html', trip=trip, user=user)

#route for processing update
@app.post('/update')
def updatetrip():
    if not Trips.validate(request.form):
            return redirect(f"/trips/edit/{id}")
    Trips.update(request.form)
    return redirect(f"/trips/{id}")

#route for viewing trip
@app.route('/trips/<int:id>')
def viewtrip(id):
    if "user_id" not in session:
        return redirect('/')
    user=Users.get_one_by_id(session["user_id"])
    trip = Trips.get_one_trip_with_users(id)
    return render_template('view.html', trip=trip, user=user)

#route for deleting trip
@app.route('/delete/<int:id>')
def deletetrip(id):
    Trips.unlink(id)
    Trips.delete(id)
    return redirect('/dashboard')

#where my trips page route would go if I had more time to figure out how to make it work.