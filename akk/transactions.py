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
    date = input('Enter the date of the transaction (YYYY-MM-DD): ')
    category = input('Enter the category of the transaction: ')
    amount = input('Enter the amount of the transaction: ')
    note = input('Enter the note: ')
    new_transaction = Transaction(date=date, category=category, amount=amount, note=note)
    session.add(new_transaction)
    session.commit()
    print('Transaction added')

# Function for calculating the total amount of a certain date
def get_total_amount_today():
    """Retrieve the total amount spent today"""
    today = input('Enter the date of the transaction (YYYY-MM-DD): ')
    query = f"SELECT SUM(amount) FROM transactions WHERE date = '{today}'"
    df = pd.read_sql(query, engine)
    return df.iloc[0][0]

def get_month_transactions():
    """Retrieve all transactions for today"""
    date = input('Enter the date of the transaction MM: ')
    month = date
    query = f"SELECT * FROM transactions WHERE EXTRACT(MONTH FROM date) = {month}"
    df = pd.read_sql(query, engine)
    # df['totals'] = get_total_amount_today()
    return df


# Function for creating a csv for dashboard
def export_to_csv():
    """Export today's transaction to a csv file"""
    date = input('Enter the date of the transaction (YYYY-MM-DD): ')
    month = date.split('-')[1]
    query = f"SELECT * FROM transactions WHERE EXTRACT(MONTH FROM date) = {month}"
    df = pd.read_sql(query, engine)
    # df['totals'] = get_total_amount_today()
    df.to_csv(f'{month}transactions.csv', index=False)


def main():
    action = input('What would you like to do? (input/today/month/csv): ')
    if action == 'i':
        add_transaction()
        print("Transactions saved successfully!")
    elif action == 'c':
        export_to_csv()
        print("Transactions saved as csv successfully!")
    elif action == 't':
        return get_total_amount_today()
    elif action == 'm':
        return get_month_transactions()
    else:
        print("Thank you!")
    
if __name__ == '__main__':
    main()