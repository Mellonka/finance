from app import app, db
from models import Expense, Category, Account, Income, Transfer
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
        notice=data['notice'].lower()
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
    record.account.balance -= record.amount * model.sign
    if record.account.name != data['account']:
        account = db.session.execute(db.select(Account).filter_by(name=data['account'])).scalar()
        record.account = account
    if record.category.name != data['category']:
        category = db.session.execute(db.select(Category).filter_by(name=data['category'])).scalar()
        record.category = category
    record.account.balance += amount * model.sign
    date = datetime.date.fromisoformat(data['date'])
    record.date = date
    record.amount = amount
    record.notice = data['notice'].lower()
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


def get_statistics(model, column, filter, date_from, date_to):
    return db.session.execute(db.select(column, db.func.sum(model.amount)).filter(column.in_(filter)).filter(
        model.date.between(date_from, date_to)).group_by(column)).all()


def record_get(model, template_name):
    categories = db.session.execute(db.select(Category).filter_by(for_expenses=bool(model.sign - 1))).all()
    accounts = db.session.execute(db.select(Account)).all()
    today = datetime.date.today()
    start_month = datetime.date(today.year, today.month, 1)
    end_month = datetime.date(today.year, today.month + 1, 1) - datetime.timedelta(1)
    if 'categories' in request.args:
        categories_ids = json.loads(request.args.get('categories'))
        categories_names = [i[0] for i in
                            db.session.execute(db.select(Category.name).filter(Category.id.in_(categories_ids)))]
    else:  # если изменить категорию то в записях оно не меняется (хз почему),
        # поэтому все записи со старыми названиями категорий не будут отображаться - надо исправить
        categories_names = [i.Category.name for i in categories]

    if 'accounts' in request.args:
        accounts_ids = json.loads(request.args.get('accounts'))
        accounts_names = [i[0] for i in
                          db.session.execute(db.select(Account.name).filter(Account.id.in_(accounts_ids)))]
    else:  # тоже самое что писал в категориях
        accounts_names = [i.Account.name for i in accounts]

    amount_from = float(request.args['amount_from']) if request.args.get('amount_from', '') != '' else float('-Inf')
    amount_to = float(request.args['amount_to']) if request.args.get('amount_to', '') != '' else float('Inf')
    date_from = datetime.date.fromisoformat(request.args['date_from']) if request.args.get('date_from',
                                                                                           '') != '' else start_month

    date_to = datetime.date.fromisoformat(request.args['date_to']) if request.args.get('date_to', '') != '' else today
    notice = request.args.get('notice', '').lower()
    records = db.session.execute(db.select(model)
                                 .filter(model.category_name.in_(categories_names))
                                 .filter(model.account_name.in_(accounts_names))
                                 .filter(model.amount.between(amount_from, amount_to))
                                 .filter(model.date.between(date_from, date_to))
                                 .filter(model.notice.like(f'%{notice}%'))
                                 .order_by(db.desc(model.id)).limit(50)).scalars()
    amount_sum = sum(
        i[0] for i in db.session.execute(db.select(model.amount).filter(model.date.between(start_month, end_month))))
    statistics_categories = get_statistics(model, model.category_name, categories_names, date_from, date_to)
    sum_categories = 0
    for _, val in statistics_categories:
        sum_categories += val

    statistics_accounts = get_statistics(model, model.account_name, accounts_names, date_from, date_to)
    sum_accounts = 0
    for _, val in statistics_accounts:
        sum_accounts += val

    return render_template(template_name, elements=records, accounts=accounts, categories=categories, today=today,
                           amount_sum=amount_sum, cat_statistics=statistics_categories, sum_cat=sum_categories,
                           acc_statistics=statistics_accounts, sum_acc=sum_accounts)


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


@app.route('/accounts', methods=['POST', 'GET', 'DELETE'])
def accounts():
    if request.method == 'POST':
        if 'id' not in request.form and 'account_from' not in request.form:
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
        elif 'account_from' in request.form:
            account_from = \
            db.session.execute(db.select(Account).filter_by(name=request.form['account_from'].lower())).first()[0]
            account_to = \
            db.session.execute(db.select(Account).filter_by(name=request.form['account_to'].lower())).first()[0]

            amount = float(request.form['amount'])
            account_from.balance -= amount
            account_to.balance += amount
            notice = request.form['notice']
            date = datetime.date.fromisoformat(request.form['date'])
            transfer = Transfer(
                amount=amount,
                account_to_=account_to,
                account_from_=account_from,
                notice=notice,
                date=date
            )
            try:
                if account_to.name == account_from.name:
                    raise Exception()
                session.pop('_flashes', None)
                db.session.add(transfer)
                db.session.commit()
                flash('Переведено успешно!', 'success')
            except:
                flash('Ошибка при переводе!', 'error')
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
            transfers = db.session.execute(db.select(Transfer).filter(Transfer.id.in_(ids))).scalars()
            for transfer in transfers:
                account_from = transfer.account_from_
                account_to = transfer.account_to_
                account_to.balance -= transfer.amount
                account_from.balance += transfer.amount
                db.session.delete(transfer)
            db.session.commit()
            flash('Все переводы успешно удалены!', 'success')
        except Exception as e:
            print(e)
            flash(
                'Ошибка при удалении!',
                'error')
        return ''
    else:
        accounts = db.session.execute(db.select(Account)).all()
        sum_accounts = db.session.execute(db.func.sum(Account.balance)).first()[0]
        today = datetime.date.today()
        transfers = db.session.execute(db.select(Transfer).order_by(db.desc(Transfer.id)).limit(50)).scalars()
        return render_template('accounts.html', transfers=transfers, accounts=accounts, today=today, sum_accounts=sum_accounts)


def login():
    pass


def register():
    pass
