import gspread 
# imports the entire gspread library
from google.oauth2.service_account import Credentials
# imports the Credentials class from google
# Every google account has a IAM cofig. Identity and Access Mannagment - Configures what can be accessed

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

sales = SHEET.worksheet('sales') 
# calls teh sales worksheet

data = sales.get_all_values()
print(data)
