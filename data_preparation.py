import pandas as pd
import numpy as np

def data_prep():
    df = pd.read_csv('kick.csv')

    # Drop irrelevant columns
    df.drop(['PurchaseID', 'PurchaseTimestamp', 'WheelTypeID', 'TopThreeAmericanName', 'Nationality', 'ForSale',
             'MMRCurrentRetailRatio'], axis=1, inplace=True, errors='ignore')

    # Divide column PuchaseDate into month and year, then drop the original column
    df['PurchaseMonth'] = pd.to_datetime(df['PurchaseDate'], dayfirst=True).dt.month
    df['PurchaseYear'] = pd.to_datetime(df['PurchaseDate'], dayfirst=True).dt.year
    df.drop(['PurchaseDate'], axis=1, inplace=True, errors='ignore')

    # Rename column 'MMRAquisitonRetailCleanPrice' to 'MMRAcquisitionRetailCleanPrice'
    df.rename(columns={'MMRAcquisitonRetailCleanPrice': 'MMRAcquisitionRetailCleanPrice'}, inplace=True)

    # In any column replace ? with NaN
    df.replace('?', np.nan, inplace=True)

    categorical_columns = ['PurchaseMonth', 'PurchaseYear', 'Auction', 'VehYear', 'Make', 'Color', 'Transmission',
                           'WheelType', 'Size', 'PRIMEUNIT', 'AUCGUART', 'VNST', 'IsOnlineSale']
    # For categorical columns: replace Nan with the mode of the column
    for col in categorical_columns:
        df[col] = df[col].fillna(df[col].mode()[0])
        df[col] = df[col].astype('category')

    # %%
    numerical_columns = ['VehOdo', 'MMRAcquisitionAuctionAveragePrice', 'MMRAcquisitionAuctionCleanPrice',
                         'MMRAcquisitionRetailAveragePrice', 'MMRAcquisitionRetailCleanPrice',
                         'MMRCurrentAuctionAveragePrice', 'MMRCurrentAuctionCleanPrice', 'MMRCurrentRetailAveragePrice',
                         'MMRCurrentRetailCleanPrice', 'VehBCost', 'WarrantyCost']

    # For numerical columns: replace Nan with the mean of the column
    for col in numerical_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].mean())
        df[col] = df[col].astype('float64')

    # Delete outliers in numerical columns using IQR method
    '''
    for col in numerical_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    '''
    # one-hot encoding
    df = pd.get_dummies(df)
    return df