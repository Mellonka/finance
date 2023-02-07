from app import app, db
from models import Expense, Category, Account, Income
from flask import request, redirect, flash, render_template, session
import datetime
import json


@app.route('/')
def main_page():
    return render_template('index.html')


def record_post(model):
    data = json.loads(request.data.decode())

    category = db.session.execute(db.select(Category).filter_by(name=data['category'].lower())).scalar()
    account = db.session.execute(db.select(Account).filter_by(name=data['account'].lower())).scalar()
    amount = float(data['amount'])
    account.balance += amount * model.sign
    record = model(
        date=datetime.date.fromisoformat(data['date']) if data['date'] != '' else datetime.date.today(),
        amount=amount,
        category=category,
        account=account,
        notice=data['notice']
    )
    try:
        session.pop('_flashes', None)
        db.session.add(record)
        db.session.commit()
        flash('Успешно добавлено!', 'success')
    except:
        flash('Ошибка при добавлении записи!', 'error')
    return ''


def record_update(model):
    data = json.loads(request.data.decode())
    data['account'] = data['account'].lower()
    data['category'] = data['category'].lower()
    record = db.session.execute(db.select(model).filter_by(id=data['id'])).scalar()

    amount = float(data['amount'])
    if record.account.name != data['account']:
        record.account.balance -= record.amount * model.sign
        account = db.session.execute(db.select(Account).filter_by(name=data['account'])).scalar()
        account.balance += amount * model.sign
        record.account = account
    if record.category.name != data['category']:
        category = db.session.execute(db.select(Category).filter_by(name=data['category'])).scalar()
        record.category = category
    date = datetime.date.fromisoformat(data['date'])
    record.date = date
    record.amount = amount
    record.notice = data['notice']
    try:
        session.pop('_flashes', None)
        db.session.commit()
        flash('Запись успешно обновлена!', 'info')
    except:
        flash('Ошибка при обновлении записи!', 'error')
    return ''


def record_delete(model):
    ids = list(map(int, json.loads(request.data.decode())['ids']))
    count = 0
    try:
        session.pop('_flashes', None)
        if len(ids) == 0:
            raise Exception
        records = db.session.execute(db.select(model).filter(model.id.in_(ids))).scalars()
        for record in records:
            record.account.balance -= record.amount * model.sign
            db.session.delete(record)
            count += 1
        db.session.commit()
        flash('Все записи успешно удалены!', 'success')
    except:
        if count == 0:
            flash('Ошибка при удалении записи!', 'error')
        else:
            flash(f'Удалено {count} записей!', 'info')
    return ''


def record_get(model, template_name):
    categories = db.session.execute(db.select(Category).filter_by(for_expenses=bool(model.sign - 1))).all()
    accounts = db.session.execute(db.select(Account)).all()
    today = datetime.date.today()
    if 'categories' in request.args:
        categories_ids = json.loads(request.args['categories'])
        categories_names = [i[0] for i in db.session.execute(db.select(Category.name).filter(Category.id.in_(categories_ids)))]
        accounts_ids = json.loads(request.args['accounts'])
        accounts_names = [i[0] for i in db.session.execute(db.select(Account.name).filter(Account.id.in_(accounts_ids)))]
        amount_from = float(request.args['amount_from']) if request.args['amount_from'] != '' else float('-Inf')
        amount_to = float(request.args['amount_to']) if request.args['amount_to'] != '' else float('Inf')
        date_from = datetime.date.fromisoformat(request.args['date_from']) if request.args['date_from'] != '' else datetime.date(2000, 1, 1)
        date_to = datetime.date.fromisoformat(request.args['date_to']) if request.args['date_to'] != '' else datetime.date.today()
        notice = request.args.get('notice')
        records = db.session.execute(db.select(model)
                                     .filter(model.category_name.in_(categories_names))
                                     .filter(model.account_name.in_(accounts_names))
                                     .filter(model.amount.between(amount_from, amount_to))
                                     .filter(model.date.between(date_from, date_to))
                                     .order_by(db.desc(model.id)).limit(50)).scalars()
    else:
        records = db.session.execute(db.select(model).order_by(db.desc(model.id)).limit(50)).scalars()

    amount_sum = sum(i[0] for i in db.session.execute(db.select(model.amount).filter(model.date.between(datetime.date(today.year, today.month, 1), datetime.date(today.year, today.month + 1, 1) - datetime.timedelta(1)))))
    return render_template(template_name, elements=records, accounts=accounts, categories=categories, today=today, amount_sum=amount_sum)


@app.route('/expense', methods=['POST', 'GET', 'DELETE', 'UPDATE'])
def expense():
    if request.method == 'POST':
        return record_post(Expense)
    elif request.method == 'UPDATE':
        return record_update(Expense)
    elif request.method == 'DELETE':
        return record_delete(Expense)
    else:
        return record_get(Expense, 'expense.html')


@app.route('/income', methods=['POST', 'GET', 'DELETE', 'UPDATE'])
def income():
    if request.method == 'POST':
        return record_post(Income)
    elif request.method == 'UPDATE':
        return record_update(Income)
    elif request.method == "DELETE":
        return record_delete(Income)
    else:
        return record_get(Income, 'income.html')


@app.route('/categories', methods=['POST', 'GET'])
def categories():
    if request.method == 'POST':
        if 'id' not in request.form:
            category = Category(
                name=request.form['name'].lower(),
                for_expenses='for_expenses' in request.form
            )
            try:
                session.pop('_flashes', None)
                db.session.add(category)
                db.session.commit()
                flash('Успешно добавлено!', 'success')
                return redirect('/categories')
            except:
                flash('Ошибка при добавлении категории!', 'error')
                return redirect('/categories')
        else:
            category = db.session.execute(db.select(Category).filter_by(id=int(request.form['id']))).scalar()
            category.for_expenses = 'for_expenses' in request.form
            category.name = request.form['name'].lower()
            try:
                session.pop('_flashes', None)
                db.session.commit()
                flash('Успешно обновлено!', 'success')
            except:
                flash('Ошибка при обновлении!', 'error')
            return redirect('/categories')
    else:
        categories = db.session.execute(db.select(Category)).scalars()
        return render_template('category.html', categories=categories)


@app.route('/accounts', methods=['POST', 'GET'])
def accounts():
    if request.method == 'POST':
        if 'id' not in request.form:
            account = Account(
                name=request.form['name'].lower(),
                balance=float(request.form['balance'])
            )
            try:
                session.pop('_flashes', None)
                db.session.add(account)
                db.session.commit()
                flash('Успешно добавлено!', 'success')
            except:
                flash('Ошибка при добавлении счёта!', 'error')
            return redirect('/accounts')
        else:
            account = db.session.execute(db.select(Account).filter_by(id=int(request.form['id']))).scalar()
            account.balance = float(request.form['balance'])
            account.name = request.form['name'].lower()
            try:
                session.pop('_flashes', None)
                db.session.commit()
                flash('Успешно обновлено!', 'success')
            except:
                flash('Ошибка при обновлении!', 'error')
            return redirect('/accounts')
    elif request.method == 'DELETE':
        ids = list(map(int, json.loads(request.data.decode())['ids']))
        try:
            session.pop('_flashes', None)
            accounts = db.session.execute(db.select(Account).filter(Account.id.in_(ids))).scalars()
            for account in accounts:
                db.session.delete(account.Account)
            db.session.commit()
            flash('Все записи успешно удалены!', 'success')
        except Exception as e:
            print(e)
            flash('Ошибка при удалении! Возможно существуют записи ссылающиеся на этот счёт. Советуем диактивировать счёт.', 'error')
        return ''
    else:
        accounts = db.session.execute(db.select(Account)).scalars()
        return render_template('accounts.html', accounts=accounts)


def login():
    pass

def register():
    pass

