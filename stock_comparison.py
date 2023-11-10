import yfinance as yf
import pandas as pd
import numpy as np
import random
import allstocks


# functions to...

# randomly pull a ticker
# def randomize_ticker():
#     rand_index = random.randint(0, allstocks.get_length())
#     # Select from the allstocks array based on randomized value integer
#     selected_ticker = allstocks.select_stock(rand_index)
#     # print("\nSelecting data for ticker "+selected_ticker)
    
#     # Return the ticker to be used in further calculations
#     return selected_ticker


# pull a summary of the ticker
def summary(ticker):
    stock = yf.Ticker(ticker)
    print(stock.info)
    
    # TODO: This returns way too much data, most of it useless for our purposes.
    # We need to limit what this function returns to the basics.


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
    

# evaluate the performance of that stock
def evaluate_performance(history):
    # Takes a dataframe returned by the get_history function
    # Evaluates performance and returns based on beginning and ending balance
    
    # TODO: Track down the point at which we get an empty array that causes errors to be
    # thrown.  Possibly from a now-worthless ticker or delisted company.
    length = len(history["Close"])
    if (history is None) | (length == 0):
        print("No history for ticker.  Retrying evaluate_performance function.")
        
        random_stock = allstocks.random_ticker(allstocks.filter_list())
        chosen_ticker = random_stock["Ticker"]
        print("\nEvaluating "+chosen_ticker+"...")
        evaluate_performance(get_history(chosen_ticker))
        return
    
    # print("\n\nLength of the history array: "+str(length))
    
    # Select the first and last closing prices from the dataframe and round to 2 decimals
    end_price = round(history["Close"].iloc[length-1], 2)
    beginning_price = round(history["Close"].iloc[0], 2)
    
    # Convert the "Date" column to datetime and format in "MM/DD/YYYY"
    history["Date"] = pd.to_datetime(history["Date"])
    history["Date"] = history["Date"].dt.strftime("%m/%d/%Y")
    
    # Store the beginning and ending dates
    beginning_date = history["Date"].iloc[0]
    ending_date = history["Date"].max()
    
    # print("\nbeginning price: $"+str(beginning_price)+"  -----  ending price: $"+str(end_price)+"\n")
    
    # Create a new column in the dataframe that calculates the percent change for each row
    # from the prior day's closing price.
    history["Pct_Chg"] = round(history["Close"].pct_change(periods=1).shift(-1) * 100, 3)

    # Trim some of the unnecessary columns and just focus in on the 3 we care about
    trimmed_history = history[["Date", "Close", "Pct_Chg"]]
    # print(trimmed_history.head(3))
    
    # Compute the cumulative return, standard deviation, annualized return, and risk-adjusted
    # return.  Then return these values in an array.
    
    stdev = round(trimmed_history["Pct_Chg"].std(), 4)
    hpr = round((end_price - beginning_price) / beginning_price * 100, 3)
    
    # TODO: Make the function resilient to differing evaluation periods.
    # num_years = len(trimmed_history["Close"]) / 365
    # annualized_return = round(hpr / num_years, 3)
    
    risk_adj_return = round(hpr / stdev, 4)
    
    # print("\n\nAnalysis for period beginning "+str(beginning_date)+" and ending "+str(ending_date)+"...")
    # print("\nStandard Deviation of % Change: ", stdev)
    # print("Holding Period Return: "+str(hpr)+"%")
    # print("Annualized return: "+str(annualized_return)+"%")
    # print("Risk-Adjusted Return: "+str(risk_adj_return)+"\n\n")
    
    # package the variables
    # NOTE: It might be more useful to store this in a dict but we can decide on that later.
    return [hpr, stdev, risk_adj_return, beginning_date, ending_date]
    

# Run the historical functions multiple times
def build_portfolio(num_stocks=10, duration="1y", benchmark="SPY"):
    # NOTE: If we want to specify differing start/end dates, this should be done at the
    # build_portfolio level and then passed down to the functions from there to keep the
    # timeframes consistent for comparison.
    
    # This initial iteration of build_portfolio would assume equal weighting of
    # each stock, and simultaneous purchase.
    # TODO: Expand on the parameters to allow flexible weights and purchase timing.
    
    print("Building portfolio...")
    
    # List to store lists of performance data and then convert to DF
    performance_data = []
    
    # Run evaluate_performance num_stocks number of times and append the resultant list to
    # the performance_data list.
    while len(performance_data) < num_stocks:
        random_stock = allstocks.random_ticker(allstocks.filter_list())
        ticker = random_stock["Ticker"]
        company_name = random_stock["Name"]
        
        i_data = evaluate_performance(get_history(ticker, period=duration))
        
        # Strip out the beginning and ending dates from the initialized i_data
        
        # Store performance data in a dictionary if there was stock data returned
        if i_data is not None:
            performance_dict = {
                "Ticker": ticker,
                "Company": company_name,
                "Category": allstocks.info_for(ticker, columns="Category Name"),
                "HPR": i_data[0],
                "Stdev": i_data[1],
                "Risk-Adj Return": i_data[2]
            }
        
            beginning_date = i_data[3]
            ending_date = i_data[4]
            performance_data.append(performance_dict)
        else:
            print("No data returned.  Re-running evaluation...")
        
    # Convert to dataframe
    performance_df = pd.DataFrame(performance_data)
        
    # Use a Dirichlet distribution to assign random weights to each row of the df that add to 100%
    # NOTE: Don't ask me how this part works; ChatGPT suggested it on the basis that it has a
    # more efficient algorithmic complexity than the way I was trying to assign weights.
    # I don't even know how to pronounce Dirichlet, or whether it's a who or a what.
    weights = np.random.dirichlet(np.ones(num_stocks), size=num_stocks) * 100
    weights = weights[0]
    weights = np.round(weights, 2)
    performance_df["Weights"] = weights
    
    # TODO: Maybe we break this out into its own function so we could run the same stocks
    # with different randomized weights, and see if we can draw any conclusions from that?
    
    # Append the benchmark 
    bench_data = evaluate_performance(get_history(benchmark, period=duration))
    bench_dict = {
                "Ticker": benchmark,
                "Company": "-- Benchmark --",
                "Category": "-- Benchmark --",
                "HPR": bench_data[0],
                "Stdev": bench_data[1],
                "Risk-Adj Return": bench_data[2],
                "Weights": 0
            }
    
    # Insert the dictionary of benchmark performance into the performance_df
    performance_df = pd.concat(
        [performance_df, pd.DataFrame([bench_dict])],
        ignore_index=True
        )
        
    # print(performance_df)
    return [performance_df, beginning_date, ending_date]

# compare the results to the benchmark (such as SPY) for the period analyzed

def portfolio_performance(df, beginning_date, ending_date):
    # Calculate the weighted average of HPR, Stdev, and Risk-Adj Return
    portfolio_return = (df["HPR"] * df["Weights"]).sum() / df["Weights"].sum()
    portfolio_sigma = (df["Stdev"] * df["Weights"]).sum() / df["Weights"].sum()
    portfolio_risk_adj_return = (df["Risk-Adj Return"] * df["Weights"]).sum() / df["Weights"].sum()
    
    # Format the results as percentages
    portfolio_return_percent = round(portfolio_return, 2)
    portfolio_sigma_percent = round(portfolio_sigma, 2)
    portfolio_risk_adj_return_percent = round(portfolio_risk_adj_return, 2)
    
    # print("\n\nFor the period beginning "+beginning_date+" and ending "+ending_date+":")
    # print("\nPortfolio wtd. average return: " + str(portfolio_return_percent) + "%")
    # print("Portfolio wtd. average sigma: " + str(portfolio_sigma_percent) + "%")
    # print("Portfolio risk-adjusted return: " + str(portfolio_risk_adj_return_percent) + "%")
    
    # Store the statistics for the weighted portfolio and their delta from the benchmark
    # in a dictionary to return along with the dataframe
    
    # Split the benchmark's data off from the other entries
    benchmark_data = df.iloc[-1]
    benchmark_hpr = benchmark_data['HPR']
    benchmark_stdev = benchmark_data['Stdev']
    benchmark_risk_adj_return = benchmark_data['Risk-Adj Return']
    
    statistics = {
        "Portfolio HPR": portfolio_return_percent,
        "Portfolio Stdev": portfolio_sigma_percent,
        "Portfolio Risk-Adj Return": portfolio_risk_adj_return_percent,
        "HPR Diff From Bench": (portfolio_return_percent - benchmark_hpr),
        "Stdev Diff From Bench": (portfolio_sigma_percent - benchmark_stdev),
        "Risk-Adj Return Diff From Bench": (portfolio_risk_adj_return_percent - benchmark_risk_adj_return)
    }
    
    # return the summary dataframe and statistics
    return [beginning_date, ending_date, df, statistics]        
        


# Calling this function executes the functions in the proper order with the correctly-placed
# arguments
def run_comparison():
    
    portfolio = build_portfolio()
    # Take the dataframe, beginning date, and ending date and run performance metrics
    performance = portfolio_performance(portfolio[0], portfolio[1], portfolio[2])
    
    # return beginning date, end date, performance df, and statistics dictionary
    # print(performance)
    return performance


# Testbed
# run_comparison()