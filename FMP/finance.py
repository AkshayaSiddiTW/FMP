import pandas as pd
import requests

# Load the CSV file into a DataFrame
csv_file_path = r'C:/Users/Akshaya/Downloads/FMP data/FMP ESG DATA/esg_2022.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

# Extract the list of tickers from the 'symbol' column
tickers_list = df['symbol'].tolist() 


def get_fin_data(ticker):
    try:
        url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?apikey=c1be0adf4239811e53c74255e93f467e"
        
        df = pd.DataFrame(requests.get(url).json())

        df = df[pd.to_datetime(df['date']).dt.year == 2015]
        df = df[df['calendarYear'] == "2015"]
        df = df.drop(columns=['date','reportedCurrency','cik','fillingDate','acceptedDate','period','sellingGeneralAndAdministrativeExpenses','otherExpenses','link','finalLink','weightedAverageShsOut','weightedAverageShsOutDil'])

        return df
    except:
        return None
    

data_frames = []
for idx, ticker in enumerate(tickers_list):
    data_frames.append(get_fin_data(ticker))
    if(idx%1000==0):
            print(idx+1)

df_combined = pd.concat(data_frames, ignore_index=True)
df_combined.to_csv('fin_2015.csv', encoding='utf-8', index=False)