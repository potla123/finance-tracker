from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    category = Column(String)
    date = Column(Date, default=datetime.date.today)

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True)
    month = Column(String)
    year = Column(Integer)
    amount = Column(Float)

class Income(Base):
    __tablename__ = "incomes"
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    source = Column(String)
    month = Column(String)
    year = Column(Integer)
