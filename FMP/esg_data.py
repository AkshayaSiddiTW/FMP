import requests
import pandas as pd


# Load the CSV file into a DataFrame

csv_file_path = r'C:\Users\Akshaya\Downloads\FMP data\FMP data\esg_2022.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

# Extract the list of tickers from the 'symbol' column
tickers_list = df['symbol'].tolist() 


def get_esg_data(stock_ticker):
    # Define the API endpoint with the stock ticker and API key
    url = f"https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data?symbol={stock_ticker}&apikey={apikey}"
    
    try:
        # Convert the response data into a dataframe
        df = pd.DataFrame(requests.get(url).json())
        
        # Extract year from the date column and filter by 2015
        df = df[pd.to_datetime(df['date']).dt.year == 2015]
        
        # Create the result list and return
        return [df['symbol'].iloc[0], 2015, df['environmentalScore'].mean(), df['socialScore'].mean(), df['governanceScore'].mean(), df['ESGScore'].mean()]
    except:
        return None


d_list=[]
for idx, line in enumerate(tickers_list):
        d_list.append(get_esg_data(line))
        if(idx%1000==0):
            print(idx+1)


new_list = [x for x in d_list if x is not None]

df1 = pd.DataFrame(new_list, columns=['symbol', 'year', 'E', 'S', 'G', "ESG"])

df1.to_csv('esg_2015.csv', encoding='utf-8', index=False)
