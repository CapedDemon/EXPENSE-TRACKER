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


# Define a Expenses model with the fields 'expense', 'expenditure', and 'date'
class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    expense = db.Column(db.String(255), nullable=False)
    expenditure = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(30), nullable=False)

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

# route to create the expenses in the expense table 
@app.route('/createExpenses', methods=['POST'])
def createExpenses():
    expensesData = request.get_json()

    # Check that all required fields are present in the request body
    if 'expense' not in expensesData or 'expenditure' not in expensesData or 'date' not in expensesData:
        return jsonify({'error': 'Missing fields'}), 400

    # creating the new field
    newExpense = Expenses(username=expensesData["username"], expense=expensesData["expense"], expenditure=expensesData["expenditure"], date=expensesData["date"])

    # Add the new expense to the database
    db.session.add(newExpense)
    db.session.commit()

    return jsonify({'message': 'Expense created successfully'}), 200

# route to get the expenses
@app.route('/showExpenses', methods=['POST','GET'])
def getExpenses():
    data = request.json
    # Get all expenses for the user from the expenses table
    expenses = Expenses.query.filter_by(username=data["username"]).all()
    
    # Create a list of dictionaries containing the expense data
    expenseList = []
    for expense in expenses:
        expenseDict = {'expense': expense.expense, 'expenditure': expense.expenditure, 'date': expense.date}
        expenseList.append(expenseDict)
    
    # Return the list of expenses in JSON format
    return jsonify({'expenses': expenseList}), 200

# route to delete the expenses
@app.route('/delete/Expenses', methods=['POST','GET'])
def delExpenses(self):
    pass


@app.route("/")
def home():
    return "this is expense tracker"

if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    app.run(debug=True)