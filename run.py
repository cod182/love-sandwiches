import gspread
# imports the entire gspread library
from google.oauth2.service_account import Credentials
# imports the Credentials class from google
# Every google account has a IAM cofig. Identity and Access Mannagment
# Configures what can be accessed
from pprint import pprint
# Score lists the API's the program should have access to in order to run
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
# Constant variables are in all caps
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input form user
    """
    # While loop will repeate until true is returned
    while True:
        print("Please enter sales data from last market")
        print("Data should be 6 numbers, seperated by commas")
        print("Example: 12,14,34,23,12,12\n")

        data_str = input("Enter Data Here: ")

        sales_data = data_str.split(",")
    
        if  validate_data(sales_data):
            print("Data is Valid")
            break
    
    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values to integers.
    Raises ValueError if string cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values] 
        # Checks that the values can be convertet to an integer
        # If length of values is not 6
        if len(values) != 6:
            # An ValueError is raised
            raise ValueError(
                f"Exatly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try agian.\n")
        return False
    
    return True
# The following 2 functions replaced with a single function update_worksheet
# def update_sales_worksheet(data):
#     """
#     Update sales worksheet, add new row with list data provided
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet('sales')
#     sales_worksheet.append_row(data)
#     print("sales worksheet updated successfully.\n")

# def update_surplus_worksheet(data):
#     """
#     Updates the surplus worksheet, add new row with surplus calculations
#     """
#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet('surplus')
#     surplus_worksheet.append_row(data)
#     print("surplus worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
    """
    Comapre sales with stock and calculate surplus

    Surplus is defined as sales figures subtracted from stock
    - Positive surplus is waste
    - Negative surplus is extras made
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet('stock').get_all_values()
    # Slices the final item of the list
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data

def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collection
    the last 5 entries for each sandwich and returns the data as a list of lists
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        # Appending columns but only the last 5 results
        columns.append(column[-5:])

    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each item, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data 

def update_worksheet(data, worksheet):
    """
    Recievs a list of integers to add to a worksheet
    Updates relevant worksheet with data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")

# Common practice to wrap all main function calls of a program in a funciton called main
def main():
    """
    Run all main function
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

# Functions must be called after they have been declared
print("Welcome to Love Sandwiches Data Automation")
main()

