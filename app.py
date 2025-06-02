from flask import Flask, jsonify , Response
import pandas as pd
import yfinance as yf
#for that dump on screen
import json
import time




app = Flask(__name__)




file= pd.read_csv("bulk.csv") #ho gya read



#we only need valid symbols , some symbol are not in bse and nse list in yfinance. make a cry 
def get_valid_symbol(symbol):
    for suffix in ['.NS', '.BO']:
        test_symbol = symbol + suffix
        try:
            data = yf.Ticker(test_symbol).history(period="1d")
            if not data.empty:
                return test_symbol
        except:
            continue
    return None





def get_volume_on_date(symbol, date):
    valid_symbol = get_valid_symbol(symbol)
    try:
        data = yf.download(valid_symbol, start=date, end=pd.to_datetime(date) + pd.Timedelta(days=1), progress=False)
        if not data.empty and 'Volume' in data.columns:
            volume_value = data['Volume'].iloc[0].item()
            print("DEBUG TYPE:", type(volume_value))  # make real usecase of data type check yeee
            return int(volume_value)
    except Exception as e:
        print(f"Error for {valid_symbol} on {date}: {e}")
    return None















 

@app.route('/bulk-deals',methods=['GET'])
def bulk_deals():
    volume_cache = {}   #only unique volume ko store ko kra looo
    results = []      #result that will converted to json at the end wow 
    quantity= file.QUANTITY
    quantity = quantity.str.replace(",", "", regex=False).astype(int)  #data needed cleaning as we are dividing quantity with volume
    unique_pairs = set(zip(file.SYMBOL, file.DATE))

    for symbol, date in unique_pairs:
        key = (symbol, date)

    # Fetch and cache volume
        if key not in volume_cache:
            volume_cache[key] = get_volume_on_date(symbol, date)

        volume = volume_cache[key]
        type(volume)
        # Filter the row for this (symbol, date)
        matching_rows = file[(file.SYMBOL == symbol) & (file.DATE == date)] #we only need that volume whos symbol and date matches

        if volume is not None:
            for _, row in matching_rows.iterrows():
                quantity = int(str(row['QUANTITY']).replace(",", ""))

                ratio = quantity / volume

                print(f"Volume for {symbol} on {date}: {volume}")
                print(f"Validity: {quantity} / {volume} = {ratio:.4%}") #4 decimal tak jana ha
                if ratio > 0.01:
                    results.append({
                        "symbol": symbol,
                        "deal_date": date,
                        "deal_volume": quantity,
                        "volume_percentage": round(ratio * 100, 2), #2 decimla tak round krna best haa
                        "buyer": row.get("BUYER", "UNKNOWN"),
                        "is_hft_filtered": False,  # update logic as needed
                        "position": row.get("POSITION", "BUY")
                    })

                  
    
        else:
            print(f"Volume not found for {symbol} on {date}\n")


    return jsonify(results)   



     
 #we need to create such function that will direct dump the data on screen on the above we have to wait to finish as this is how return works

@app.route('/fast-dump', methods=['GET'])
def fast_dump():
    def generate():
        volume_cache = {}
        quantity = file.QUANTITY
        quantity = quantity.str.replace(",", "", regex=False).astype(int)
        unique_pairs = set(zip(file.SYMBOL, file.DATE))

        for symbol, date in unique_pairs:
            key = (symbol, date)

            if key not in volume_cache:
                volume_cache[key] = get_volume_on_date(symbol, date)

            volume = volume_cache[key]

            matching_rows = file[(file.SYMBOL == symbol) & (file.DATE == date)]

            if volume is not None:
                for _, row in matching_rows.iterrows():
                    quantity = int(str(row['QUANTITY']).replace(",", ""))

                    ratio = quantity / volume

                    if ratio > 0.01:
                        result = {
                            "symbol": symbol,
                            "deal_date": date,
                            "deal_volume": quantity,
                            "volume_percentage": round(ratio * 100, 2),
                            "buyer": row.get("BUYER", "UNKNOWN"),
                            "is_hft_filtered": False,
                            "position": row.get("POSITION", "BUY")
                        }

                        # Stream one JSON result at a time
                        yield f"data: {json.dumps(result)}\n\n"
                        time.sleep(0.1)  # Optional: slow down output for visibility

            else:
                yield f"data: Volume not found for {symbol} on {date}\n\n"
                time.sleep(0.05)

    return Response(generate(), mimetype='text/event-stream')




@app.route("/valid-symbols", methods=["GET"])
def valid_symbols():
    
    for symbol in file.SYMBOL:
        valid_symbol = get_valid_symbol(symbol)
        if valid_symbol:
            print(valid_symbol)
        else:
            print(f"Invalid symbol: {symbol}")




    




if __name__ == "__main__":
    app.run(debug=True)