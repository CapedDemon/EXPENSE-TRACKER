from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
db = SQLAlchemy(app)

# The user model
# consits only id, username and password
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# register route
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    # takes a post request and json data

    # checks whether user is present or not
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User with this username already exists! Try Again'}), 400


    user = User(username=data['username'], password=data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully! Press L to login'}), 200

# login route
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    # checks whether the username and password is present or not
    user = User.query.filter_by(username=data['username'], password=data['password']).first()

    if user:
        return jsonify({'message': 'Access Granted'}), 200
    else:
        return jsonify({'message': 'Access Denied'}), 401

@app.route("/")
def home():
    return "this is expense tracker"

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)