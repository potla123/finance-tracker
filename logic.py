from db import Expense, Income, Session
import datetime

# --- Expense functions ---
def add_expense(amount, category, date):
    with Session() as session:
        expense = Expense(amount=amount, category=category, date=date)
        session.add(expense)
        session.commit()

def get_all_expenses():
    with Session() as session:
        expenses = session.query(Expense).order_by(Expense.date.desc()).all()
    return expenses

# --- Income functions ---
def add_income(amount, source, month, year):
    with Session() as session:
        existing = session.query(Income).filter_by(month=month, year=year).first()
        if existing:
            existing.amount = amount
            existing.source = source
        else:
            income = Income(amount=amount, source=source, month=month, year=year)
            session.add(income)
        session.commit()

def get_all_incomes():
    with Session() as session:
        incomes = session.query(Income).order_by(Income.year.desc(), Income.month.desc()).all()
    return incomes
