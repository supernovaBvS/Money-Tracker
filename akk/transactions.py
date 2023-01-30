import psycopg2
from sqlalchemy import create_engine, Column, Integer, Float, String, Date, func
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from datetime import datetime

# # Connect to the database
# connection = psycopg2.connect(
#     host="localhost",
#     user="postgres",
#     password="postgres",
#     database="transaction"
# )

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
    reward = Column(Float)
    amount = Column(Float)
    note = Column(String)

# Create the transactions table in the database
Base.metadata.create_all(engine)


# Function for inputting a new transaction
def add_transaction():
    from sqlalchemy.orm import sessionmaker
    # Create a session to add and query data
    Session = sessionmaker(bind=engine)
    session = Session()
    reward = 0
    amount = 0
    date = input('Enter the date of the transaction (YYYY-MM-DD): ')
    # date = datetime.now()
    cat = ['trans', 'food', 'drink', 'shop', 'ran', 'sell', 'reward']
    category = cat[int(input("trans=0, food=1, drink=2, shop=3, ran=4, sell=5, reward=6: "))]
    if category == cat[5] or category == cat[6]:
        reward = input('Enter the HKD of the transaction: ')
    else:
        amount = input('Enter the HKD of the transaction: ')
    note = input('Enter the note: ')
    new_transaction = Transaction(date=date, category=category, reward=reward, amount=amount, note=note)
    session.add(new_transaction)
    session.commit()
    print('Transaction added')

# Function for calculating the total amount of a certain date
def get_total_amount_to_day():
    """Retrieve the total amount spent today"""
    today = input('Enter the date of the transaction (YYYY-MM-DD): ')
    query = f"SELECT SUM(amount) FROM transactions WHERE date = '{today}'"
    df = pd.read_sql(query, engine)
    return df.iloc[0][0]


def get_total_amount_to_month(month):
    """Retrieve the total amount spent today"""
    query = f"SELECT SUM(amount) FROM transactions WHERE EXTRACT(MONTH FROM date) = {month}"
    df = pd.read_sql(query, engine)
    return df.iloc[0][0]


def get_total_reward_to_month(month):
    """Retrieve the total reward spent today"""
    query = f"SELECT SUM(reward) FROM transactions WHERE EXTRACT(MONTH FROM date) = {month}" 
    df = pd.read_sql(query, engine)
    return df.iloc[0][0]


def get_month_transactions():
    """Retrieve all transactions for monthly"""
    month = int(input('Enter the month of the transaction: '))
    a = get_total_reward_to_month(month)
    b = get_total_amount_to_month(month)
    query = f"SELECT * FROM transactions WHERE EXTRACT(MONTH FROM date) = {month}"
    df = pd.read_sql(query, engine)
    df.at[0, 'totalsR'] = a
    df.at[0, 'totalsA'] = b
    # df.at[2, 'totals'] = a-b``
    df['totalsR'] = df['totalsR'].fillna('')
    df['totalsA'] = df['totalsA'].fillna('')
    df = df[['date', 'category', 'reward', 'amount', 'note', 'totalsR',
       'totalsA']]
    return df.sort_values(by='date', ascending=False)


# Function for creating a csv for dashboard
def export_to_csv():
    """Export month's transaction to a csv file"""
    month = int(input('Enter the month of the transaction: '))
    a = get_total_reward_to_month(month)
    b = get_total_amount_to_month(month)
    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    query = f"SELECT * FROM transactions WHERE EXTRACT(MONTH FROM date) = {month}"
    df = pd.read_sql(query, engine)
    df.at[0, 'totalsR'] = a
    df.at[0, 'totalsA'] = b
    # df.at[2, 'totals'] = a-b
    
    df['totalsR'] = df['totalsR'].fillna('')
    df['totalsA'] = df['totalsA'].fillna('')
    df = df[['date', 'category', 'reward', 'amount', 'note', 'totalsR',
       'totalsA']]
    df.to_csv(f'{months[month]} transactions.csv', index=False)


def main():
    while True:
        action = input('What would you like to do? (input=i/today=t/month=m/csv=c): ')
        if action.upper() == 'I':
            add_transaction()
            print("Transactions saved successfully!")
        elif action.upper() == 'C':
            export_to_csv()
            print("Transactions saved as csv successfully!")
        elif action.upper() == 'T':
            print(get_total_amount_to_day())
        elif action.upper() == 'M':
            print(get_month_transactions())
        else:
            print("Thank you!")
        cont = input("Do you want to continue (Y/N)?")
        if cont.upper() == 'N':
            break
    

if __name__ == '__main__':
    main()