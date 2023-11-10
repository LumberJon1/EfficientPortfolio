        price_data["Date"] = pd.to_datetime(price_data["Date"]).dt.strftime("%m/%d/%Y")
        price_data["Close"] = round(price_data["Close"], 2)