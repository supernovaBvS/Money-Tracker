import psycopg2
from sqlalchemy import create_engine, Column, Integer, Float, String, Date, func
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import datetime

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
    income = Column(Float)
    outcome = Column(Float)
    note = Column(String)

# Create the transactions table in the database
Base.metadata.create_all(engine)


# Function for inputting a new transaction
def add_transaction():
    """Adds a new transaction to the database.

    Prompts the user to enter the transaction details, such as the transaction date, category,
    income/outcome amount, and note. The function then creates a new Transaction object with
    the entered details and adds it to the database.

    Returns:
    None
    """
    from sqlalchemy.orm import sessionmaker
    # Create a session to add and query data
    Session = sessionmaker(bind=engine)
    session = Session()
    income = 0
    outcome = 0
    d = input('today=t or specified date=s or yesterday=y? ').upper()
    if d == 'T':
        date = datetime.now()
    elif d == 'Y':
        date = datetime.datetime.now().date() - datetime.timedelta(days=1)
    else:
        date = input('Enter the date of the transaction (YYYY-MM-DD): ')
    cat = ['trans', 'food', 'drink', 'shop', 'others', 'sell', 'income']
    category = cat[int(input("trans=0, food=1, drink=2, shop=3, others=4, sell=5, income=6: "))]
    if category == cat[5] or category == cat[6]:
        income = input('Enter the HKD of the transaction: ')
    else:
        outcome = input('Enter the HKD of the transaction: ')
    note = input('Enter the note: ')
    new_transaction = Transaction(date=date, category=category, income=income, outcome=outcome, note=note)
    session.add(new_transaction)
    session.commit()
    print('Transaction added')


# Function for calculating the total amount of a certain date
def get_total_amount_to_day():
    """
    Retrieves the total amount spent for a specific date.

    Args:
    - month (int): The number of the month for which to retrieve the total amount spent.

    Returns:
    - The total amount spent for the specified month as a float.

    Raises:
    - None

    Example:
    >>> get_total_amount_to_day(2023-02-28) returns 500.0 
    if the total amount spent in 2023-02-28 is 500.0.
    """
    d = input('today=t or specified date=s or yesterday=y? ').upper()
    if d == 'T':
        today = datetime.now()
    elif d == 'Y':
        today = datetime.datetime.now().date() - datetime.timedelta(days=1)
    else:
        today = input('Enter the date of the transaction (YYYY-MM-DD): ')
    query = f"SELECT SUM(outcome) FROM transactions WHERE date = '{today}'"
    df = pd.read_sql(query, engine)
    return df.iloc[0][0]


def get_total_amount_to_month(month):
    """
    Retrieve the total amount spent in the given month.

    Args:
        month (int): The month for which to retrieve the total amount spent (1-12).

    Returns:
        float: The total amount spent in the given month, as a float.

    Raises:
        None.

    Examples:
        >>> get_total_amount_to_month(1)
        100.0
        >>> get_total_amount_to_month(12)
        250.0
    """
    query = f"SELECT SUM(outcome) FROM transactions WHERE EXTRACT(MONTH FROM date) = {month}"
    df = pd.read_sql(query, engine)
    return df.iloc[0][0]


def get_total_reward_to_month(month):
    """
    Retrieve the total income spent in a given month.

    Args:
    month (int): The month to retrieve the total income spent for. Should be a number between 1 and 12.

    Returns:
    float: The total income spent for the given month.

    Raises:
    None.

    Examples:
    >>> get_total_reward_to_month(1)
    500.0

    """
    query = f"SELECT SUM(income) FROM transactions WHERE EXTRACT(MONTH FROM date) = {month}" 
    df = pd.read_sql(query, engine)
    return df.iloc[0][0]


def get_month_transactions():
    """
    Retrieve all transactions for a specific month, including the total income and total expenses.
    
    Returns:
        pandas.DataFrame: A pandas DataFrame containing the transactions for the specified month, sorted in descending order by date. 
                           The DataFrame contains the following columns: date, category, income, outcome, note, totalsR, totalsA.
                           The totalsR and totalsA columns show the total income and total expenses for the specified month, respectively.
    """
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
    df = df[['date', 'category', 'income', 'outcome', 'note', 'totalsR',
       'totalsA']]
    return df.sort_values(by='date', ascending=False)


'''

def forjanny():














'''


# Function for creating a csv for dashboard
def export_to_csv():
    """
    Export month's transaction to a csv file

    This function prompts the user to enter the month of the transactions they would like to export, then retrieves all transactions
    for that month from the database, calculates the total income and outcome for the month and adds these totals to the dataframe. 
    The resulting dataframe is sorted by date in descending order and exported to a csv file named after the month in the format
    '<Month Name> transactions.csv'. The csv file is saved to the current working directory.

    Parameters:
    None

    Returns:
    None
    """
    month = int(input('Enter the month of the transaction: '))
    a = get_total_reward_to_month(month)
    b = get_total_amount_to_month(month)
    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    query = f"SELECT * FROM transactions WHERE EXTRACT(MONTH FROM date) = {month} order by date DESC"
    df = pd.read_sql(query, engine)
    df.at[0, 'totalsR'] = a
    df.at[0, 'totalsA'] = b
    # df.at[2, 'totals'] = a-b
    
    df['totalsR'] = df['totalsR'].fillna('')
    df['totalsA'] = df['totalsA'].fillna('')
    df = df[['date', 'category', 'income', 'outcome', 'note', 'totalsR',
       'totalsA']]
    df.to_csv(f'{months[month]} transactions.csv', index=False)


def main():
    while True:
        action = input('What would you like to do? (input=i/today=t/month=m/csv=c): ').upper()
        if action == 'I':
            add_transaction()
            print("Transactions saved successfully!")
        elif action == 'C':
            export_to_csv()
            print("Transactions saved as csv successfully!")
        elif action == 'T':
            print(get_total_amount_to_day())
        elif action == 'M':
            print(get_month_transactions())
        else:
            print("Thank you!")
        if input("Do you want to continue (Y/N)?").upper() == 'N':
            break
    

if __name__ == '__main__':
    main()