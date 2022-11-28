from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)   
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite///database/expenseTracker.db'
app.config["SECRET_KEY"] = "blah"


class ExpenseTrackerUser(db.Model, UserMixin):
    pass

@app.route('/')
def home():
    return "SUI"

if __name__ == '__main__':
    app.run(debug=True)
    