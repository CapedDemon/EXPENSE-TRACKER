from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

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
    user = User.query.filter_by(username=data['username'], password=data['password']).first()

    if user:
        return jsonify({'message': 'Access Granted'}), 200
    else:
        return jsonify({'message': 'Access Denied'}), 401

# route to create the expenses in the expense table 
@app.route('/createExpenses', methods=['POST'])
def createExpenses():
    expensesData = request.get_json()
    if 'expense' not in expensesData or 'expenditure' not in expensesData or 'date' not in expensesData:
        return jsonify({'error': 'Missing fields'}), 400
    newExpense = Expenses(username=expensesData["username"], expense=expensesData["expense"], expenditure=expensesData["expenditure"], date=expensesData["date"])
    db.session.add(newExpense)
    db.session.commit()

    return jsonify({'message': 'Expense created successfully'}), 200

# route to get the expenses
@app.route('/showExpenses', methods=['POST','GET'])
def getExpenses():
    data = request.json
    expenses = Expenses.query.filter_by(username=data["username"]).all()
    
    expenseList = []
    for expense in expenses:
        expenseDict = {'expense': expense.expense, 'expenditure': expense.expenditure, 'date': expense.date}
        expenseList.append(expenseDict)
    
    return jsonify({'expenses': expenseList}), 200

# route to delete the expenses
@app.route('/deleteExpenses', methods=['POST','GET'])
def delExpenses():
    data = request.json
    if data["identification1"] == "expense":
        if data["identification2"] == "expenditure":
            result = Expenses.query.filter_by(username=data["username"], expenditure=data["value2"], expense=data["value1"]).delete()

        if data['identification2'] == "date":
            result = Expenses.query.filter_by(username=data["username"], date=data["value2"], expense=data["value1"]).delete()

    elif data["identification1"] == "expenditure":
        if data["identification2"] == "expense":
            result = Expenses.query.filter_by(username=data["username"], expenditure=data["value1"], expense=data["value2"]).delete()

        if data['identification2'] == "date":
            result = Expenses.query.filter_by(username=data["username"], date=data["value2"], expenditure=data["value1"]).delete()

    if data["identification1"] == "date":
        if data["identification2"] == "expenditure":
            result = Expenses.query.filter_by(username=data["username"], expenditure=data["value2"], date=data["value1"]).delete()

        if data['identification2'] == "expense":
            result = Expenses.query.filter_by(username=data["username"], date=data["value1"], expense=data["value2"]).delete()

    if result:
        db.session.commit()
        return jsonify({'message': 'Successfully deleted'}), 200
    else:
        return jsonify({'message': 'Could not delete'}), 400

# route for updating the records
@app.route("/updateExpenses", methods=["GET", "POST"])
def updateExpense():
    data = request.json
    if data["identification"] == "expense":
        if data["changed"] == "expenditure":
            updated = Expenses.query.filter_by(username=data["username"], expense=data["value"]).update(dict(expenditure=data["changedValue"]))
        if data["changed"] == "date":
            updated = Expenses.query.filter_by(username=data["username"], expense=data["value"]).update(dict(date=data["changedValue"]))

    elif data["identification"] == "data":
        if data["changed"] == "expenditure":
            updated = Expenses.query.filter_by(username=data["username"], date=data["value"]).update(dict(expenditure=data["changedValue"]))
        if data["changed"] == "expense":
            updated = Expenses.query.filter_by(username=data["username"], date=data["value"]).update(dict(expense=data["changedValue"]))

    elif data["identification"] == "expenditure":
        if data["changed"] == "expenditure":
            updated = Expenses.query.filter_by(username=data["username"], expenditure=data["value"]).update(dict(expense=data["changedValue"]))
        if data["changed"] == "date":
            updated = Expenses.query.filter_by(username=data["username"], expenditure=data["value"]).update(dict(date=data["changedValue"]))

    if updated:
        db.session.commit()
        return jsonify({'message': 'Successfully updated'}), 200
    else:
        return jsonify({'message': 'Could not be updated'}), 400

# deleting your whole account
@app.route("/deleteAccount", methods=["GET"])
def delAccount():
    data = request.json
    userExpense = Expenses.query.filter_by(username=data['username']).first()

    if userExpense:
        deleteExpense = Expenses.query.filter_by(username=data["username"]).delete()

        if deleteExpense:
            db.session.commit()

    else:
        delUser = User.query.filter_by(username=data["username"]).delete()

        if delUser:
            db.session.commit()
            return jsonify({'message': 'Successfully loggedout', 'del':delUser}), 200
        else:
            return jsonify({'message': 'Could not delete account', 'del':delUser}), 400


@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    db.create_all()
    app.run(host = "0.0.0.0")