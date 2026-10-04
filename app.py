from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    ratings = db.relationship('Rating', backref='user', lazy=True)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
          return redirect(url_for('profile', username=username))

        return 'Invalid username or password. Please try again.'  

    return render_template('index.html')
    
@app.route('/profile')
def profile():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()

    if user is None:
        return "User not found."
    
    else:
        return render_template('profile.html', username=username, media=Rating.query.filter_by(user_id=user.id).all())

@app.route('/addRating', methods=['POST', 'GET'])
def addRating():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        user = User.query.filter_by(username=username).first()

        if user is None:
            return "User not found.", 404

        mediaName = request.form.get('name', '').strip()

        ratingValue = request.form.get('rating', '').strip()

        new_rating = Rating(
            name=mediaName,
            rating=ratingValue,
            user_id=user.id
        )
        db.session.add(new_rating)
        db.session.commit()

        return redirect(url_for('profile', username=user.username))

    username = request.args.get('username', '')
    return render_template('addRating.html', username=username)



   

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return "Username already exists. Please choose a different username."

        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/index', methods=['POST', 'GET'])
def back():
    if request.method == 'POST':
        return redirect(url_for('index'))
    
    return render_template('index.html')

@app.route('/delete/<username>/<int:rating_id>', methods=['POST','GET'])
def delete(username,rating_id):
    rating = Rating.query.get_or_404(rating_id)
    db.session.delete(rating)
    db.session.commit()
    return redirect(url_for('profile', username=username))

@app.route('/edit/<username>/<int:rating_id>', methods=['POST', 'GET'])
def editRating(username, rating_id):
    rating = Rating.query.get_or_404(rating_id)
    if request.method == 'POST':
        rating.name = request.form['name']
        rating.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('profile', username=username))
    return render_template('editRating.html', username=username, rating=rating)

if __name__ == '__main__':
    app.run(debug=True)



       