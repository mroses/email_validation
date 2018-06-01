from flask import Flask, request, redirect, render_template, session, flash
from datetime import datetime
from time import time
app = Flask(__name__)
app.secret_key = 'mysecretkey'

from mysqlconnection import MySQLConnector
mysql = MySQLConnector(app, 'email_validation_db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    email_address = request.form['email'] #sets up variable for what is entered in form
    session['email'] = email_address #uses session
    query = "SELECT email FROM users WHERE email = :email"
    data = {
        'email': email_address #request.form['email']
    }
    user_email = mysql.query_db(query, data)
    #section above queries for any emails in the DB that match the email recently entered in the form on index.html. If statement below then decides what to do next based on a few conditions..

    if len(user_email) == 0: #if there is no email in DB that matches email entered in form:
        query = "INSERT INTO users (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = {
            'email': email_address #request.form['email']
        }
        mysql.query_db(query, data) #inserts new email from form in the DB
        flash("The Email you entered {}".format(request.form['email']) + " " + "is a valid email!", 'success')
        return redirect('/success')
    else: #entered email did match an email in the DB so len of user_email was not 0
        flash("Email is not valid!",'error')
        return redirect('/')

@app.route('/success')
def success():
    query = ("SELECT id, email, DATE_FORMAT(created_at, '%m/%d/%y %I:%m %p') AS date FROM users")
    all_users=mysql.query_db(query)
    return render_template('success.html', users=all_users)
app.run(debug=True)
