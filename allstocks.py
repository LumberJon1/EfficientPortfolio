import pandas as pd
import random
import os
import yfinance as yf
        
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
    
    
# pull historical prices for that stock
def get_history(ticker, interval="1d", period="1y"
                # start_date="2023-01-01", end_date="2023-09-14"
                ):
    # Interval can be "1d", "5d", "1wk", "1mo", or "3mo"
    # start and end are given in str, dt, or int: "YYYY-MM-DD", datetime, or epoch respectively.
    # Alternatively, we can use a period argument in place of start and end dates.
    # period can equal "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", or "max".
    
    # TODO: Validate based on duration and/or interval to prevent out-of-bounds dates
    
    stock = yf.Ticker(ticker)
    history = stock.history(interval=interval, period=period
                            # start=start_date, end=end_date
                            )
    
    # if len(history) == 0:
    #     print("No history available.")
    #     return
    
    # Reset index to make Date accessible
    history = history.reset_index()
    # print(history)
    
    # Return the dataframe
    return history

    
    
# Filters the already-filtered csv returned from writeToFilteredCSV and 
# only stores those symbols which have data in yfinance
def writeContentfulTickers():
    raw_df = pd.read_csv(os.path.join(project_dir, "filtered_stocks.csv"))
    
    # Trim df to just symbols
    essential_df = raw_df.iloc[:, 1:2]
    
    print(essential_df.head())
    # Convert to dict
    symbols_dict = essential_df.to_dict()
    # print(symbols_dict)
    
    # list which will hold price data and store until df creation at the end of the function
    contentful_tickers = pd.DataFrame({})
    
    #  --development environment flag to limit yfinance API calls:
    iterCounter = 0
    
    for item in symbols_dict["Ticker"].values():
        if (iterCounter <= 10):
            ticker = item
            print("\nsearching for price data for "+item+"...")
            
            # Call the getPriceData function
            priceData = get_history(ticker=ticker)
            
            # Evaluate whether any data was returned.
            if (priceData.empty):
                print("Empty return - no price data")
                
            else:
                # If there is data, store in a new dataframe
                print(priceData.head(2))
                priceData = priceData[["Date", "Close"]]
                
                priceData["Ticker"] = ticker
                
                # Convert the "Date" column to datetime and format in "MM/DD/YYYY"
                priceData["Date"] = pd.to_datetime(priceData["Date"])
                priceData["Date"] = priceData["Date"].dt.strftime("%m/%d/%Y")
                
                # Round prices to 2 decimals
                priceData["Close"] = round(priceData["Close"], 2)
                
                # Append to contentful_tickers
                contentful_tickers = pd.concat([contentful_tickers, priceData], axis=1)

                print(priceData)
            
            iterCounter += 1
            print("\nContentful Tickers: \n"+str(contentful_tickers))
            
        # Exit once counter has been reached
        else:
            print("Development environment API call limit reached")
            break
        
    
    # Write the finished dataframe to the same path, overwriting the previous filtered CSV
    print(contentful_tickers.head(15))
    
    contentful_tickers.to_csv(path_or_buf=os.path.join(project_dir, "price_history.csv"))
    


writeToFilteredCSV()
writeContentfulTickers()

