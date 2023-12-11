########## FUNCTIONS TO GET DATA FROM MARKETWATCH ##########
##############################
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os 
os.chdir('C:/Users/ene/documents/FinancePython/')
# import scrapeMktwatch as smw
import datetime, requests

def get_financial_info(ticker):
    # Get date
    today = datetime.date.today().strftime('%Y%m%d')

    # Construct the URL
    url = f"https://www.marketwatch.com/investing/stock/{ticker}/company-profile?mod=mw_quote_tab"

    # Send a GET request to the server
    response = requests.get(url)


    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the content of the response
        page_content = response.content

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(page_content, 'lxml')

        # Find the financial metrics in the BeautifulSoup object
        bases = soup.find_all('div', attrs={'class' : 'element element--table'})
        
        all_data=[]
        for base in bases:
            section = base.find_all('tr', attrs={'class' : 'table__row'})
    
            for item in section:
                data = {}
                data['name']=item.td.text
                data['value']=item.td.findNext('td').text
                data['date'] = today
                data['ticker'] = ticker
                all_data.append(data)

        # Return all the data
        return all_data      

    else:
        return None
    

def get_cashflow(ticker): 
    # Get date
    today = datetime.date.today().strftime('%Y%m%d')
    
    # Construct the URL
    url2 = f"https://www.marketwatch.com/investing/stock/{ticker}/financials/cash-flow"

    # Send a GET request to the server
    response = requests.get(url2)
    
    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the content of the response
        page_content = response.content

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(page_content, 'lxml')

        # Find the table in the HTML
        table = soup.find('table', attrs={'aria-label':'Financials - Operating Activities data table'})

        # Extracting the years
        header = table.find('thead')
        header_cells = header.find_all('th')
        years = [cell.div.text for cell in header_cells[1:6]] # Assuming the first 5 cells after 'Item' contain the years

        # Find all rows in the table
        rows = table.find_all('tr')

        # Create a list to store all the data
        data = []

        # Iterate over each row
        for row in rows:
            row_data = {}
            cells = row.find_all('td') # Find all table cells in a row
            if cells: 
                name = cells[0].div.text # The variable name is in the first cell
                values = [cell.div.text for cell in cells[1:6]] # Extracting the values
                # Combining name, years and values
                for year, value in zip(years, values):
                    row_data = {'name': name, 'year': year, 'value': value, 'ticker': ticker}
                    data.append(row_data)

        # Now 'data' contains the last 6 columns of each row in the table.
        
    # Return all the data
        return data      

    else:
        return None
    
def get_balancesheets(ticker): 
    # Get date
    today = datetime.date.today().strftime('%Y%m%d')
    
    # Construct the URL
    url3 = f"https://www.marketwatch.com/investing/stock/{ticker}/financials/balance-sheet"

    # Send a GET request to the server
    response = requests.get(url3)
    
    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the content of the response
        page_content = response.content

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(page_content, 'lxml')

        # Find the table in the HTML
        table = soup.find('table', attrs={'aria-label':'Financials - Assets data table'})

        # Extracting the years
        header = table.find('thead')
        header_cells = header.find_all('th')
        years = [cell.div.text for cell in header_cells[1:6]] # Assuming the first 5 cells after 'Item' contains the years

        # Find all rows in the table
        rows = table.find_all('tr')

        # Create a list to store all the data
        data = []

        # Iterate over each row
        for row in rows:
            row_data = {}
            cells = row.find_all('td') # Find all table cells in a row
            if cells: 
                name = cells[0].div.text # The variable name is in the first cell
                values = [cell.div.text for cell in cells[1:6]] # Extracting the values
                # Combining name, years and values
                for year, value in zip(years, values):
                    row_data = {'name': name, 'year': year, 'value': value, 'ticker': ticker}
                    data.append(row_data)

        # Now 'data' contains the last 6 columns of each row in the table.
        
    # Return all the data
        return data      

    else:
        return None


def get_financialssheet(ticker): 
    # Get date
    today = datetime.date.today().strftime('%Y%m%d')
    
    # Construct the URL
    url4 = f"https://www.marketwatch.com/investing/stock/{ticker}/financials?mod=mw_quote_tab"

    # Send a GET request to the server
    response = requests.get(url4)
    
    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the content of the response
        page_content = response.content

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(page_content, 'lxml')

        # Find the table in the HTML
        table = soup.find('table', attrs={'aria-label':'Financials - data table'})

        # Extracting the years
        header = table.find('thead')
        header_cells = header.find_all('th')
        years = [cell.div.text for cell in header_cells[1:6]] # Assuming the first 5 cells after 'Item' contains the years

        # Find all rows in the table
        rows = table.find_all('tr')

        # Create a list to store all the data
        data = []

        # Iterate over each row
        for row in rows:
            row_data = {}
            cells = row.find_all('td') # Find all table cells in a row
            if cells: 
                name = cells[0].div.text # The variable name is in the first cell
                values = [cell.div.text for cell in cells[1:6]] # Extracting the values
                # Combining name, years and values
                for year, value in zip(years, values):
                    row_data = {'name': name, 'year': year, 'value': value, 'ticker': ticker}
                    data.append(row_data)

        # Now 'data' contains the last 6 columns of each row in the table.
        
    # Return all the data
        return data      

    else:
        return None


# Convert string percentages to floats
def convert_percentage(val):
    try:
        if isinstance(val, str):
            return float(val.strip('%')) / 100
        return val
    except:
        return val
    
# Convert strings to floats
def convert_value(value):
    if isinstance(value, str):
        try:
            if value[-1] == 'B':
                return float(value[:-1]) * 1e9
            elif value[-1] == 'M':
                return float(value[:-1]) * 1e6
            elif value[-1] == '%':
                return float(value[:-1]) / 100
            elif value == '-':
                return 0.0
            elif value[0] == '(' and value[-1] == ')':
                return -float(value[1:-1])
            else:
                return float(value)
        except ValueError:
            pass
    return value

   