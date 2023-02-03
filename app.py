from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SECRET_KEY'] = '5a3a08a0bb92afca394bbec133b4dfd7'
CORS(app)
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)

import views