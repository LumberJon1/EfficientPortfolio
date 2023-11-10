import pandas as pd
import random
import os
        
# Path variables for use with files and CSV methods
filepath = os.path.abspath(__file__)
project_dir = os.path.dirname(filepath)

# Relative paths to CSV files
all_symbols_path_stocks = "/AllSymbolsv2_Stocks.csv"
all_symbols_path_etfs = "/AllSymbolsv2_ETFs.csv"


def filter_list(list="Stocks", country="USA"):
    print("path: "+project_dir+all_symbols_path_stocks)
    # Will read the AllSymbols CSV files (defaults to just stocks) and then organize
    # them to filter out ADRs, international stocks, etc. and create a dataframe of just
    # usable tickers to pass to the search and comparison functions
    
    # Check which list we are using and create DF appropriately
    if list == "Stocks":
        raw_df = pd.read_csv(project_dir+all_symbols_path_stocks)
        
    else:
        raw_df = pd.read_csv(all_symbols_path_etfs)
        
    # check out the columns
    # print(raw_df.columns)
    
    # We only care about the first 5 columns, so we will shrink the df to that size
    essential_df = raw_df.iloc[:, :5]
    
    # By default, sort for just US-based tickers, but return whichever country
    # parameter is selected.
    country_specific_df = essential_df[essential_df["Country"] == country]
    
    # Filter out tickers for ADRs or non-standard share classes, etc.
    # Conditions might include 5-letter tickers that end in Q, F, or Y
    filtered_df = country_specific_df[
        ~country_specific_df["Ticker"].str.endswith(("Q", "F", "Y"))
        ]
    
    # print(country_specific_df.head(20))
    return filtered_df
    
    
# Return a randomized stock or ETF row from a filtered dataframe (returned by the
# filter_list function) for use in main.py
def random_ticker(filtered_list):
    
    # Select a random index from the filtered list
    rand_index = random.randint(0, len(filtered_list["Ticker"]))
    selected_stock = filtered_list.iloc[rand_index]
    
    # Package into a dictionary to return
    stock_dictionary = selected_stock.to_dict()
    return stock_dictionary



def info_for(ticker, columns="all"):
    # returns info from any or all columns from the CSV for a particular ticker.
    
    print("\nStock CSV filepath: "+abs_path_stocks)
    raw_df = pd.read_csv(abs_path_stocks)
        
    # Trim to only the columns with meaningful data
    trimmed_df = raw_df.iloc[:, :5]
    
    # Return any and all columns the parameter is asking for
    stock_data = (trimmed_df.loc[trimmed_df["Ticker"] == ticker])
    if (columns == "all"):
        print(stock_data[["Ticker", "Name", "Exchange", "Category Name", "Country"]])
        return stock_data[["Ticker", "Name", "Exchange", "Category Name", "Country"]]
        
    else:
        print(stock_data[[columns]])
        return stock_data[columns]
        
            
# Test the filter and write function
def writeToFilteredCSV():
    
    # Take a filtered list of US-only companies' stocks
    filtered_df = filter_list()
    
    filtered_df.to_csv(path_or_buf=os.path.join(project_dir, "filtered_stocks.csv"))
    
    
    
# Filters the already-filtered csv returned from writeToFilteredCSV and 
# only stores those symbols which have data in yfinance
def writeContentfulTickers():
    raw_df = pd.read_csv(os.path.join(project_dir, "filtered_stocks.csv"))
    
    # Trim df to just symbols
    essential_df = raw_df.iloc[:, 1:2]
    
    print(essential_df.head())
    
    # Iterate through each of the symbols and call yfinance data
    
    
    # If there is data, store in a new dataframe
    
    # Else, continue
    
    # Write the finished dataframe to the same path, overwriting the previous filtered CSV
    
    


writeToFilteredCSV()
writeContentfulTickers()

