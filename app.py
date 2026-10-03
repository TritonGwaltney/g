from asyncio import tasks

from flask import Flask, redirect, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

users = {}
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)



with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = users.get(username)

        if password_hash and check_password_hash(password_hash, password):
          return redirect(url_for('profile', username=username))

        return 'Invalid username or password. Please try again.'  

    return render_template('index.html')
    
@app.route('/profile')
def profile():
    username = request.args.get('username')
    return render_template('profile.html', username=username)



   

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']

        if username in users:
            return "Username already exists. Please choose a different username."

        users[username] = generate_password_hash(password)
        
        return redirect(url_for('index'))
    else:
        print("Rendering signup page")

    
    
    return render_template('signup.html')

@app.route('/index', methods=['POST', 'GET'])
def back():
    if request.method == 'POST':
        return redirect(url_for('index'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



       