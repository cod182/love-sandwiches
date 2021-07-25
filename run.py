import gspread
# imports the entire gspread library
from google.oauth2.service_account import Credentials
# imports the Credentials class from google
# Every google account has a IAM cofig. Identity and Access Mannagment
# Configures what can be accessed
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

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with list data provided
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print("sales worksheet updated successfully.\n")


data = get_sales_data()
sales_data = [int(num) for num in data]
update_sales_worksheet(sales_data)