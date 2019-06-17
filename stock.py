from flask import Flask, render_template, redirect, request, session, flash, jsonify
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt 
import re
import requests

app = Flask(__name__)
#Instantiate BCrypt
bcrypt = Bcrypt(app)
#Establish Secret Key for session
app.secret_key = ")4-A'CPZzcbpzp#S]?U^f)sBjDXQW=HrE,#+#9SQ8OUr[QU$dE$n0qm]wf,j9?Y"
#Email Regex Formula
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
@app.route('/')
def index():
    print("GET: Index HTML")
    return render_template('index.html')

@app.route('/login')
def login():
    print("GET: Login HTML")
    return render_template('login.html')

@app.route('/register')
def register():
    print("GET: Register HTML")
    return render_template('register.html')

@app.route('/faq')
def faq():
    print("GET: FAQ HTML")
    return render_template('faq.html')

@app.route('/dashboard')
def dashboard():
    print("GET: Dashboard HTML")
    return render_template('dashboard.html')

@app.route('/watchlist')
def watchlist():
    print("GET: Watchlist HTML")
    return render_template('watchlist.html')

@app.route('/settings')
def settings():
    print("GET: Settings HTML")
    return render_template('settings.html')

@app.route('/logout')
def logout():
    print("GET: Logout")
    session.clear()
    return redirect('/')

#Register - Validation
@app.route('/register_submit', methods=['POST'])
def register_submit():
    #CREATE
    valid = True
    #Determine Flash Error Messages
    if len(request.form['first_name']) < 1:
        flash("Please enter a first name.")
        valid = False
    if request.form['first_name'].isdigit():
        flash("First name must contain only letters.")
        valid = False
    if len(request.form['last_name']) < 1:
        flash("Please enter a last name.")
        valid = False
    if request.form['last_name'].isdigit():
        flash("Last name must contain only letters.")
        valid = False
    if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        flash("Please enter a valid email address.", 'email')
        valid = False
    if request.form['password'] != request.form['confirm_password']:
        flash("Passwords do not match.")
        valid = False
    if len(request.form['password']) < 5:
        flash("Password must be longer than 5 characters.")
        valid = False
    #Determine if User Already Exists by Email
    db = connectToMySQL('vesta')
    validate_email_query = 'SELECT id FROM users WHERE email=%(email)s;'
    form_data = {
        'email': request.form['email']
    }
    existing_users = db.query_db(validate_email_query, form_data)
    if existing_users:
        ("Email is already in use.")
        valid = False
    #If Error Then: Redirect to Home Page
    #Do Not Create User
    if not valid:
        return redirect('/register')
    #If No Errors Then Add to Database
    #Create a Session ID based on the Database User ID
    if not '_flashes' in session.keys():	# there are no errors
        #Reconnect to MySQL for create function.
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        db = connectToMySQL('vesta')
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(fn)s, %(ln)s, %(em)s, %(pw)s);'
        data = {
            'fn': request.form['first_name'],
            'ln': request.form['last_name'],
            'em': request.form['email'],
            'pw': pw_hash
        }
        db.query_db(query, data)
        session.clear()
        print("Registered Correctly!")
    return redirect("/login")

#Login - Validation
@app.route('/login_submit', methods=['POST'])
def login_submit():
    db = connectToMySQL("vesta")
    #READ
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { "email" : request.form["email"] }
    result = db.query_db(query, data)
    error = None
    if result:
        # assuming we only have one user with this username, the user would be first in the list we get back
        # of course, we should have some logic to prevent duplicates of usernames when we create users
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            # if we get True after checking the password, we may put the user id in session
            # never render on a post, always redirect!
            print("Successful Login")
            session['first_name'] = result[0]["first_name"]
            session['last_name'] = result[0]["last_name"]
            session['email'] = result[0]["email"]
            session['user_id'] = result[0]["id"]
            print("Session User ID: " + str(session['user_id']))
            return redirect("/dashboard")
    # If Email Doesn't Exist or If the Passwords Don't Match
    # Flash an Error Message and Return to Home Page
    error = 'Invalid username or password. Please try again!'
    print("Unsuccessful Login")
    return render_template("login.html", error = error)

#DELETE
@app.route('/settings_submit', methods=['POST'])
def delete():
    if request.form['settings_button'] == 'Delete':
        print("DELETE")
        db = connectToMySQL("vesta")
        query = 'DELETE FROM users WHERE (id = %(item_id)s);'
        data = {
                'item_id' : session['user_id']
            }
        db.query_db(query, data)
        session.clear()
        return redirect('/')
        #UPDATE
    elif request.form['settings_button'] == 'Update':
        valid = True
        #Determine Flash Error Messages
        if len(request.form['first_name']) < 1:
            flash("Please enter a first name.")
            valid = False
        if request.form['first_name'].isdigit():
            flash("First name must contain only letters.")
            valid = False
        if len(request.form['last_name']) < 1:
            flash("Please enter a last name.")
            valid = False
        if request.form['last_name'].isdigit():
            flash("Last name must contain only letters.")
            valid = False
        if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
            flash("Please enter a valid email address.", 'email')
            valid = False
        if request.form['password'] != request.form['confirm_password']:
            flash("Passwords do not match.")
            valid = False
        if len(request.form['password']) < 5:
            flash("Password must be longer than 5 characters.")
            valid = False
        #Do Not Create User
        if not valid:
            return redirect('/settings')
        #If No Errors Then Add to Database
        #Create a Session ID based on the Database User ID
        if not '_flashes' in session.keys():	# there are no errors
            pw_hash = bcrypt.generate_password_hash(request.form['password'])
            db = connectToMySQL('vesta')
            query = 'UPDATE users SET first_name = %(fn)s, last_name = %(ln)s, email = %(em)s, password = %(pw)s WHERE (id = %(user_id)s);'
            data = {
                'fn': request.form['first_name'],
                'ln': request.form['last_name'],
                'em': request.form['email'],
                'pw': request.form['password'],
                'user_id' : session['user_id']
            }
            db.query_db(query, data)
            return redirect('/settings')
if __name__ == '__main__':
    app.run(debug=True)