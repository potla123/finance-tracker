from db import Expense, Session
import datetime

def add_expense(amount, category, date):
    session = Session()
    expense = Expense(amount=amount, category=category, date=date)
    session.add(expense)
    session.commit()
    session.close()

def get_all_expenses():
    session = Session()
    expenses = session.query(Expense).order_by(Expense.date.desc()).all()
    session.close()
    return expenses
