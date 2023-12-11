
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os 
os.chdir('C:/Users/ene/documents/FinancePython/')
# import scrapeMktwatch as smw
import datetime, requests
import ScrapeMarketwatchFunctions01ene as smf


########## WRANGLE THE DATA ##########
##############################
ass = 'C:/Users/ene/documents/FinancePython/'
today = datetime.date.today().strftime('%Y%m%d')

########## SPY  SPY ##########
# Add SPY to get better estimates of mean and var of the metrics
url = "https://www.ssga.com/us/en/intermediary/etfs/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx"
INPUT_FILE = ass + 'stockLists/SPY/' + today + '_holdings-daily-us-en-spy.xlsx'
response = requests.get(url)
with open(INPUT_FILE, 'wb') as f:
    f.write(response.content)
    

# note: nrows DOES NOT INCLUDE HEADER IN COUNT
df = pd.read_excel(INPUT_FILE, skiprows=4, nrows=506)

# List to store all the dataframes
dfs = []
for j in range(1,df.shape[0]):
    data = smf.get_financial_info(df.Ticker[j])
    df1 = pd.DataFrame(data)
    dfs.append(df1)

# Concatenate all the dataframes into a single dataframe
final_df = pd.concat(dfs)

# Apply the conversion function to the 'value' column
final_df['value'] = final_df['value'].apply(smf.convert_percentage)

# Convert the 'value' column to numeric format (this will fail for non-numeric strings)
final_df['value'] = pd.to_numeric(final_df['value'], errors='coerce')

# Pivot the final dataframe to have one column for each 'name'
final_df = final_df.pivot_table(index=['ticker', 'date'], columns='name', values='value')

# Reset the index to have 'ticker' and 'date' as columns again
final_df = final_df.reset_index()

metricsDF = final_df
metricsDF.to_csv(ass + 'tests/' + today + '_SPY.csv', index=False)

# List to store all the dataframes for cash flow data
dfs = []
error_count = 0
for j in range(1,df.shape[0]):
    try:
        data = smf.get_cashflow(df.Ticker[j])
        df1 = pd.DataFrame(data)
        dfs.append(df1)
    except AttributeError:
        error_count += 1
        print(f"An error occurred at index {j}. Total errors: {error_count}")
        continue

# Concatenate all the dataframes into a single dataframe
cashflow_df = pd.concat(dfs)

# Apply the conversion function to the 'value' column
cashflow_df['value'] = cashflow_df['value'].apply(smf.convert_value)

# Convert the 'value' column to numeric format (this will fail for non-numeric strings)
cashflow_df['value'] = pd.to_numeric(cashflow_df['value'], errors='coerce')

# Pivot the final dataframe to have one column for each 'name'
cashflow_df = cashflow_df.pivot_table(index=['ticker','year'], columns='name', values='value')

# Reset the index to have 'ticker' and 'date' as columns again
cashflow_df = cashflow_df.reset_index()

cashflow_df.to_csv(ass + 'tests/' + today + 'cashflow_SPY.csv', index=False)


# List to store all the dataframes for balance sheet data
dfs = []
error_count = 0
for j in range(1,df.shape[0]):
    try:
        data = smf.get_balancesheets(df.Ticker[j])
        df1 = pd.DataFrame(data)
        dfs.append(df1)
    except AttributeError:
        error_count += 1
        print(f"An error occurred at index {j}. Total errors: {error_count}")
        continue

# Concatenate all the dataframes into a single dataframe
balancesheet_df = pd.concat(dfs)

# Apply the conversion function to the 'value' column
balancesheet_df['value'] = balancesheet_df['value'].apply(smf.convert_value)

# Convert the 'value' column to numeric format (this will fail for non-numeric strings)
balancesheet_df['value'] = pd.to_numeric(balancesheet_df['value'], errors='coerce')

# Pivot the final dataframe to have one column for each 'name'
balancesheet_df = balancesheet_df.pivot_table(index=['ticker','year'], columns='name', values='value')

# Reset the index to have 'ticker' and 'date' as columns again
balancesheet_df = balancesheet_df.reset_index()

balancesheet_df.to_csv(ass + 'tests/' + today + 'balancesheet_SPY.csv', index=False)


# List to store all the dataframes for finance sheet data
dfs = []
error_count = 0
for j in range(1,df.shape[0]):
    try:
        data = smf.get_financialssheet(df.Ticker[j])
        df1 = pd.DataFrame(data)
        dfs.append(df1)
    except AttributeError:
        error_count += 1
        print(f"An error occurred at index {j}. Total errors: {error_count}")
        continue

# Concatenate all the dataframes into a single dataframe
financesheet_df = pd.concat(dfs)

# Apply the conversion function to the 'value' column
financesheet_df['value'] = financesheet_df['value'].apply(smf.convert_value)

# Convert the 'value' column to numeric format (this will fail for non-numeric strings)
financesheet_df['value'] = pd.to_numeric(financesheet_df['value'], errors='coerce')

# Pivot the final dataframe to have one column for each 'name'
financesheet_df = financesheet_df.pivot_table(index=['ticker','year'], columns='name', values='value')

# Reset the index to have 'ticker' and 'date' as columns again
financesheet_df = financesheet_df.reset_index()

financesheet_df.to_csv(ass + 'tests/' + today + 'financesheet_SPY.csv', index=False)
########## METRIC SCORE CALCULATIONS ##########
##############################
# net income from cash flow divided by net margin gives sales and sales multiplied by EV/Sales gives EV to calculate EV/NOCF. For Profitibality use return on equity/assets or NOCF/TotalEquity
balancesheet_df = pd.read_csv('C:/Users/ene/Documents/FinancePython/tests/20230626balancesheet_SPY.csv')
cashflow_df = pd.read_csv('C:/Users/ene/Documents/FinancePython/tests/20230624cashflow_SPY.csv')
metricsDF = pd.read_csv('C:/Users/ene/Documents/FinancePython/tests/20230622_SPY.csv')
financesheet_df = pd.read_csv('C:/Users/ene/Documents/FinancePython/tests/20230622financesheet_SPY.csv')

metricsDF.loc[:, 'date'] = pd.to_datetime(metricsDF['date'], format='%Y%m%d')

cashflow_df = cashflow_df.sort_values(['ticker', 'year'], ascending=[True, False])
cashflow_df = cashflow_df.drop_duplicates(subset='ticker', keep='first')

balancesheet_df = balancesheet_df.sort_values(['ticker', 'year'])
balancesheet_df['asset_growth'] = balancesheet_df.groupby('ticker')['Total Assets'].pct_change()
balancesheet_df = balancesheet_df.drop_duplicates(subset='ticker', keep='last')

balancesheet_df = balancesheet_df.drop(['year'], axis=1)
metricsDF = metricsDF.drop(['date'], axis=1)

df_merge = metricsDF.merge(cashflow_df, on=['ticker'], how='outer')
df_merge = df_merge.merge(balancesheet_df, on=['ticker'], how='outer')

df_merge['EV'] = (df_merge['Net Income before Extraordinaries'] / df_merge['Net Margin']) * df_merge['Enterprise Value to Sales']
df_merge['EV/NOCF'] = (df_merge['EV'] / df_merge['Net Operating Cash Flow']) 
df_merge['NOCF/Total Assets'] = (df_merge['Net Operating Cash Flow'] / df_merge['Total Assets']) 

VARS = ['P/E Current', 'Price to Book Ratio', 'Enterprise Value to Sales', 'Enterprise Value to EBITDA', 'EV/NOCF', 'Return on Assets', 'asset_growth','NOCF/Total Assets']

KEEP = ['ticker','year'] + VARS  
df_merge = df_merge[KEEP]
    
negativeReplacements = pd.Series(index=VARS)
negativeReplacements['P/E Current'] = df_merge.loc[df_merge['P/E Current']>0, 'P/E Current'].quantile(0.84)
negativeReplacements['Price to Book Ratio'] = df_merge.loc[df_merge['Price to Book Ratio']>0, 'Price to Book Ratio'].quantile(0.97)
negativeReplacements['Enterprise Value to Sales'] = df_merge.loc[df_merge['Enterprise Value to Sales']>0, 'Enterprise Value to Sales'].quantile(0.84)
negativeReplacements['Enterprise Value to EBITDA'] = df_merge.loc[df_merge['Enterprise Value to EBITDA']>0, 'Enterprise Value to EBITDA'].quantile(0.92)
negativeReplacements['EV/NOCF'] = df_merge.loc[df_merge['EV/NOCF']>0, 'EV/NOCF'].quantile(0.84)
# lowest 11% is the same as highest 89% of the negative of profitability
negativeReplacements['Return on Assets'] = df_merge.loc[df_merge['Return on Assets']>0, 'Return on Assets'].quantile(0.12)
negativeReplacements['asset_growth'] = 0.0
negativeReplacements['NOCF/Total Assets'] = df_merge.loc[df_merge['NOCF/Total Assets']>0, 'NOCF/Total Assets'].quantile(0.12)


meanSeries = pd.Series(index=['new'+v for v in VARS])
stdSeries = pd.Series(index=['new'+v for v in VARS])

for var in VARS:
    df_merge.loc[df_merge[var] >= 0, 'new'+var] = df_merge.loc[df_merge[var] >= 0, var]
    df_merge.loc[(df_merge[var] < 0) | (df_merge[var].isna()), 'new'+var] = negativeReplacements[var]
    if var not in ['Return on Assets', 'NOCF/Total Assets']:
        df_merge.loc[df_merge[var].isnull(), 'new'+var] = df_merge['new'+var].quantile(0.6)
    elif var in ['Return on Assets', 'NOCF/Total Assets']:
        df_merge.loc[df_merge[var].isnull(), 'new'+var] = df_merge['new'+var].quantile(0.4)
        
    meanSeries['new'+var] = df_merge['new'+var].mean()
    stdSeries['new'+var] = df_merge['new'+var].std()
    df_merge['Z_' + var] = (df_merge['new' + var] - meanSeries['new' + var])/stdSeries['new'+var]




df_merge['multiIndex'] =  -0.33*df_merge['Z_Price to Book Ratio'] - 0.66/3 * df_merge['Z_P/E Current'] - 0.66/3* df_merge['Z_Enterprise Value to Sales'] - 0.66/6 *df_merge['Z_Enterprise Value to EBITDA'] - 0.66/6 * df_merge['Z_EV/NOCF'] + 0.5*df_merge['Z_NOCF/Total Assets'] + 0.5*df_merge['Z_Return on Assets'] - 0.7*df_merge['Z_asset_growth']

df_merge = df_merge.sort_values(by='multiIndex')
KEEP = ['Z_' + var for var in VARS]+['multiIndex','ticker','year']
df_merge_toprint = df_merge[KEEP]
df_merge_toprint.to_csv(ass + 'tests/' + today + '_df_merge_sorted.csv', index=False)

 