from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

# Database connection
engine = create_engine("sqlite:///finance.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Table structure
class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    category = Column(String)
    date = Column(Date, default=datetime.date.today)

# Create tables
Base.metadata.create_all(engine)
