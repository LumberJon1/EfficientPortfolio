import pandas as pd
import random
import os
        

# CSV path - change project directory and relative path accordingly if needed
project_dir = "C:/Users/Jonathan/Desktop/Bootcamp/Python/"
relative_path_v1 = "StockMarketComparison/allstocks.csv"
all_symbols_path_stocks = "StockMarketComparison/AllSymbolsv2_Stocks.csv"
all_symbols_path_etfs = "StockMarketComparison/AllSymbolsv2_ETFs.csv"

# "C:/Users/Jonathan/Desktop/Bootcamp/Python/StockMarketComparison/AllSymbolsv2_Stocks.csv"

# Join paths for each csv
abs_path_1 = os.path.join(project_dir, relative_path_v1)
abs_path_stocks = os.path.join(project_dir, all_symbols_path_stocks)
abs_path_etfs = os.path.join(project_dir, all_symbols_path_etfs)


# Validate path before opening and log an error if not exists.
if os.path.exists(abs_path_1) == False:
    print("\nThe filepath {abs_path_1} does not exist.  Check file directory.".format(abs_path_1=abs_path_1))

else:
    
    # Perform necessary transformations and create methods
    stocks = pd.read_csv(abs_path_1)
    # print(stocks.head(10))
    # print(stocks.columns)

    #     
    def check_in_stocks(ticker):
        
        matching_stock = stocks[stocks["ACT Symbol"] == ticker]
        
        if len(matching_stock) > 0:
            company_name = matching_stock["Company Name"].values[0]
            # print("\n\n"+ticker, "\n"+company_name+"\n\n")
            # Return the ticker and company name if it's in the csv file
            return [ticker, company_name]

        else:
            print("\n\n"+ticker+" is not in the list of stock symbols.\n\n")
            
    
    # Function to pass the length of the CSV and allow a randomization not to exceed
    # array length and be out of bounds
    def get_length():
        series_length = len(stocks["ACT Symbol"])
        return series_length
            
            
    # Function to return the stock based on an index passed as an argument
    def select_stock(index):
        selected_stock = stocks["ACT Symbol"].iloc[index]
        # print("\nSelected stock: "+selected_stock)
        
        # TODO: Add some validation to exclude ADRs etc.
        
        return selected_stock
    
        
# select_stock(6)
# get_length()
# check_in_stocks("AA")



# ------------------------------------------------------------------------------------

# These functions below will use the v2 symbols list, while those above use the older allstocks.csv

    def filter_list(list="Stocks", country="USA"):
        print("path: "+project_dir+all_symbols_path_stocks)
        # Will read the AllSymbols CSV files (defaults to just stocks) and then organize
        # them to filter out ADRs, international stocks, etc. and create a dataframe of just
        # usable tickers to pass to the search and comparison functions
        
        # Check which list we are using and create DF appropriately
        if list == "Stocks":
            
            raw_df = pd.read_csv(
                "C:/Users/Jonathan/Desktop/Bootcamp/Python/StockMarketComparison/AllSymbolsv2_Stocks.csv")
            
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
        raw_df = pd.read_csv(
                "C:/Users/Jonathan/Desktop/Bootcamp/Python/StockMarketComparison/AllSymbolsv2_Stocks.csv")
            
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
        
            
        