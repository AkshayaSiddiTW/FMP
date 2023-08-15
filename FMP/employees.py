import pandas as pd
import requests

# Load the CSV file into a DataFrame
csv_file_path = r'C:/Users/Akshaya/Downloads/FMP data/Esg Data/esg_2022.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

# Extract the list of tickers from the 'symbol' column
tickers_list = df['symbol'].tolist() 


def get_emp_count(ticker):
    try:
        url = f"https://financialmodelingprep.com/api/v4/historical/employee_count?symbol={ticker}&apikey=c1be0adf4239811e53c74255e93f467e"

        df = pd.DataFrame(requests.get(url).json())
        df = df[pd.to_datetime(df['periodOfReport']).dt.year == 2015]
        df = df.drop(columns = ['cik', 'acceptanceTime', 'periodOfReport', 'formType', 'filingDate', 'source'])

        return df
    except:
        return None
    

data_frames = []
for idx, ticker in enumerate(tickers_list):
    data_frames.append(get_emp_count(ticker))
    if(idx%1000==0):
            print(idx+1)

df_combined = pd.concat(data_frames, ignore_index=True)

# Filter out rows with zero employee counts from df_combined
df_combined = df_combined[df_combined['employeeCount'] != 0]

df_combined.to_csv('emp_2015.csv', encoding='utf-8', index=False)