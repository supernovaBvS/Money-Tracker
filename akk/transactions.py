import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, Date, func
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import datetime
from datetime import datetime

# Connect to the database
connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="postgres",
    database="transaction"
)

# Create a SQLAlchemy engine to handle database operations
engine = create_engine('postgresql://postgres:postgres@localhost:5432/transaction')

# Create a base class for declarative models
Base = declarative_base()

# Define the transaction model
class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    category = Column(String)
    amount = Column(Integer)
    note = Column(String)

# Create the transactions table in the database
Base.metadata.create_all(engine)


# Function for inputting a new transaction
def add_transaction():
    from sqlalchemy.orm import sessionmaker
    # Create a session to add and query data
    Session = sessionmaker(bind=engine)
    session = Session()
    # date = input('Enter the date of the transaction (YYYY-MM-DD): ')
    date = datetime.now().date()
    category = input('Enter the category of the transaction: ')
    amount = input('Enter the amount of the transaction: ')
    note = input('Enter the note: ')
    new_transaction = Transaction(date=date, category=category, amount=amount, note=note)
    session.add(new_transaction)
    session.commit()
    print('Transaction added')

# Function for calculating the total amount of a certain date
def get_today_transactions():
    """Retrieve all transactions for today"""
    today = datetime.now().date()
    query = f"SELECT * FROM transactions WHERE date = '{today}'"
    df = pd.read_sql(query, engine)
    return df

def get_total_amount_today():
    """Retrieve the total amount spent today"""
    today = datetime.now().date()
    query = f"SELECT SUM(amount) FROM transactions WHERE date = '{today}'"
    df = pd.read_sql(query, engine)
    return df.iloc[0][0]


# Function for creating a csv for dashboard
def export_to_csv():
    """Export today's transaction to a csv file"""
    today = datetime.now().date()
    query = f"SELECT * FROM transactions WHERE date = '{today}'"
    df = pd.read_sql(query, engine)
    df.to_csv(f'{today}transactions.csv', index=False)

while True:
    action = input('What would you like to do? (input/csv): ')
    if action == 'i':
        add_transaction()
    elif action == 'c':
        export_to_csv()
    else:
        print("Transactions saved successfully!")
        break
    
