import yfinance as yf
import pandas as pd
import numpy as np
import random
import stock_comparison
import allstocks


# 

# functions to...

# Run the stock_comparison functions multiple times and store the results as a dataframe
def randomize_portfolios(num_iterations=5, beginning_date="", period=""):
    # TODO: Set default beginning and period parameters that will influence the date range
    # for the randomized portfolios
    
    # Create storage for comparison results
    results_list = []
    
    # Run the portfolio comparisons num_iterations times
    for i in range(num_iterations):
       comparison_i = stock_comparison.run_comparison()
       
        # NOTE: Dict seems like a good datatype for storage because of differing returned datatypes
        # and the ability to label them: dataframe, summary dict, beginning and end dates.
       results_list.append({
           "beginning date": comparison_i[0],
           "end date": comparison_i[1],
           "dataframe": comparison_i[2],
           "statistics dict": comparison_i[3]
       })
       
    # Return the results list
    print(results_list[0]["dataframe"])
    return results_list
       
       
# Analyze the characteristics of the compared randomized portfolios
def analyze_portfolios(portfolio_list):
    # Create a storage dataframe to hold the analysis
    columns = ["median_hpr", "median_risk", "median_under_over", "median_risk_prem"]
    analysis_df = pd.DataFrame(columns=columns)
    
    # Iterate through the portfolio list and create a dataframe that summarizes key statistics
    # from each of the dataframes, such as:
    for item in portfolio_list:
        df = item[2]
    
    # What was the median under/overperformance of a randomized portfolio compared to its
    # benchmark?
        

    
    # What was the median risk premium over the benchmark for a randomized portfolio?
    
    # Were there any patterns in categories/sectors and risk or return measures?
    # Maybe a value_count or sorted df of the df["category name"] series for each?
    
    # Write the summary statistics dataframe to a CSV file within the output folder
    


# Testbed
randomize_portfolios(1)
