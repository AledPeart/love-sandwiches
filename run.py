import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:

        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")
        
        if validate_data(sales_data): 
            print("Data is valid!")
            break 
    return sales_data



def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values] #list comprehension to convert stings to ints
        if len(values) != 6: 
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

'''
def update_sales_worksheet(data):
    
    update sales worksheet, add new row with the list data provided.
    

    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated succesfully.\n")

def update_surplus_worksheet(data):
    
    update surplus worksheet, adds a new row with new surplus data
    

    print("Updating surplus worksheet...\n")
     surplus_worksheet = SHEET.worksheet("surplus")
     surplus_worksheet.append_row(data)
     print("Surplus worksheet updated succesfully.\n")
'''
#following code is a function that uses re-factoring to amalgamate the above functions into one and reduce repetition
def update_worksheet(data, worksheet):
    '''
    updates both surplus and sales worksheet, adds a new row with new surplus/sales data
    '''

    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated succesfully.\n")



def calculate_surplus_data(sales_row):
    '''
        Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    '''

    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1] #slices and returns the last row from "stock"

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data

def get_last_5_entries_sales():
    """ 
    collects columns of data from sales worksheet, 
    colllecting the last 5 entries for each sandwich
    and returns the data as a list of lists.
    """

    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    calculates the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data =[]

    for column in data:
        int_column = [int(num) for num in column] 
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data

def get_stock_values(data):
    '''
    function to return a dictionary of sandwich headings and stock values
    '''
    headings = SHEET.worksheet("stock").row_values(1)
    
    
    stock_dictionary = {i:j for i, j in zip(headings, data)}
    
    

    print (f"Make the following numbers of sandwiches for the next market: \n {stock_dictionary}")



def main():
    '''
    Run all program functions
    '''

    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    stock_values = get_stock_values(stock_data)

print("Welcome to Love Sandwiches Data Automation")
main()






