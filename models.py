from app import db, app
import datetime


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.date.today)
    amount = db.Column(db.Float, nullable=False)
    notice = db.Column(db.String(300), nullable=True)

    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # user = db.relationship('User', backref=db.backref('expenses', lazy=True))

    account_name = db.Column(db.String, db.ForeignKey('account.name'), nullable=False)
    account = db.relationship('Account', backref=db.backref('expenses', lazy=True))

    category_name = db.Column(db.String, db.ForeignKey('category.name'), nullable=False)
    category = db.relationship('Category', backref=db.backref('expenses', lazy=True))

    sign = -1

    def __repr__(self):
        return '<Expense %r>' % self.id


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    for_expenses = db.Column(db.Boolean, nullable=False)

    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # user = db.relationship('User', backref=db.backref('categories', lazy=True))

    def __repr__(self):
        return '<Category %s>' % self.name


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0)
    #
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # user = db.relationship('User', backref=db.backref('accounts', lazy=True))

    def __repr__(self):
        return '<Account %s>' % self.name


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.date.today)
    amount = db.Column(db.Float, nullable=False)
    notice = db.Column(db.String(300), nullable=True)

    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # user = db.relationship('User', backref=db.backref('incomes', lazy=True))

    account_name = db.Column(db.String, db.ForeignKey('account.name'), nullable=False)
    account = db.relationship('Account', backref=db.backref('incomes', lazy=True))

    category_name = db.Column(db.String, db.ForeignKey('category.name'), nullable=False)
    category = db.relationship('Category', backref=db.backref('incomes', lazy=True))

    sign = 1

    def __repr__(self):
        return '<Income %r>' % self.id


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     login = db.Column(db.String(50), nullable=False, unique=True)
#     password = db.Column(db.String(100), nullable=False)
#
#     # email = db.Column(db.String(100), unique=True)
#
#     def __repr__(self):
#         return '<User %r>' % self.id
