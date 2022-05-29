from flask import Flask, current_app
from flask import render_template
from flask import request, redirect, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from initial import users
import bcrypt
import secrets
import os

app = Flask(__name__)


app.config['MONGO_URI'] = "mongodb+srv://admin:121301Traym@cluster0.3yqtr.mongodb.net/Social?retryWrites=true&w=majority"

mongo = PyMongo(app)

#mongo.db.create_collection('social-web')

 
app.secret_key = secrets.token_urlsafe(16)
#mongo.db.create_collection('social-web')
#db.create_collection(“employees”)
@app.route('/')
#want to add public or private section where user can decided with they want there post to be public or private

@app.route('/begin', methods=['GET', 'POST'])
def begin():
    return render_template('begin.html')

@app.route("/seed")
def seed():
    collection = mongo.db.users
    collection2 = mongo.db.posts
    collection.insert_one({"first name": "admin", "last name": "1", "email": "admin@gmail.com", "username": "admin1", "password":"1234"})
    collection2.insert_one({"name":"admin", "post":"I like to code", "type":"Public"})
    return "OK"


'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    else:
        users = mongo.db.users

        email = request.form['email']
        password = request.form['password'].encode("utf-8")

        login_user = users.find_one({'email': email})

        if login_user:
            current_password = login_user['password']

            if bcrypt.checkpw(password, current_password):
                session['username'] = request.form['username']
                current_user = request.form['email']

                return redirect(url_for('homepage'))
            
            else:
                return 'Invalid username/password combination.'

        else:
            return "User not found"
            
#sign-up to site
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    else:
        users = mongo.db.users

        first_name = request.form['first_name']
        last_name = request.form['last_name']

        email = request.form['email']
        #confirm_email = request.form['confirm_email_address']

        password = request.form['password']
        #confirm_password = request.form['confirm_password']

        existing_user = users.find_one({'email': email})

        if not existing_user:

        #if email != confirm_email:
        #    return "Your email does not match"

        #elif password != confirm_password:
        #    return "Passwords does not match"
            username = request.form['username']
            #encode password for hashing
            password = request.form['password'].encode("utf-8")
            #hash password
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password, salt)
            #add new user to database
            users.insert_one({"first name": first_name, "last name": last_name, 'email': email, 'name': username, 'password': hashed})
            
            #store username in session
            session['username'] = request.form['username']
            current_user = request.form['username']
            return redirect(url_for('homepage'))

        else:
            return 'Account already exists. Try logging in.'



#view a list of people you follow
@app.route('/following/<user>')
def following(user):
  collection = mongo.db.profile
  profile = collection.find({"username":user})
  return render_template('following.html', profile=profile)


#posts 
@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'GET':
        types = ['Public', 'Private']
        return render_template('post.html',types=types)

    else:
        name = session['username']
        post = request.form['post']
        type = request.form['type'] 
        collection = mongo.db.posts

  
        collection.insert_one({"name":name, "post":post, "type":type})

        return redirect(url_for('feed'))
#posts 

@app.route('/explore')
def explore():
  collection = mongo.db.posts
  posts = collection.find({"type":"Public"})
  return render_template('explore.html', posts=posts)

#view people's post you follow
@app.route('/feed/<user>')
def feed(user):
  collection = mongo.db.posts
  users = mongo.db.user
  account = users.find({"username": user})
  following = account.following
  posts = collection.find({"name": following})

  return render_template('feed.html', posts=posts, user=user)






@app.route('/profile/<user>')
def profile(user):
    return render_template('profile.html', user=user)


'''
