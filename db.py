from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

# Database connection
engine = create_engine("sqlite:///finance.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Models

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

# Create tables (if not exist)
Base.metadata.create_all(engine)
