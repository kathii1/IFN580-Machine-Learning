import pandas as pd
import numpy as np


def data_prep():
    '''
    Load and clean the kick.csv dataset.

    - Drops irrelevant and redundant columns.
    - Extracts month/year from PurchaseDate and fixes column typos.
    - Replaces placeholders ('?', 'NOT AVAIL') and invalid IsOnlineSale codes with NaN.
    - Converts VehYear to integer, imputes missing values
      (mode for categoricals, mean for numericals).
    - Returns cleaned DataFrame with lists of numerical and categorical columns.
    '''

    df = pd.read_csv('kick.csv', low_memory=False)

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

    # Replace invalid numbers with NaN in IsOnlineSale
    df['IsOnlineSale'] = df['IsOnlineSale'].replace(['-1', '2', '4'], np.nan)

    # Replace NOT AVAIL with NaN in Color
    df['Color'] = df['Color'].replace('NOT AVAIL', np.nan)

    # Convert VehYear from float to int
    df['VehYear'] = df['VehYear'].astype('Int64')

    categorical_columns = ['PurchaseMonth', 'PurchaseYear', 'Auction', 'VehYear', 'Make', 'Color', 'Transmission',
                           'WheelType', 'Size', 'PRIMEUNIT', 'AUCGUART', 'VNST', 'IsOnlineSale']
    # For categorical columns: replace Nan with the mode of the column
    for col in categorical_columns:
        df[col] = df[col].fillna(df[col].mode()[0])
        df[col] = df[col].astype('category')

    numerical_columns = ['VehOdo', 'MMRAcquisitionAuctionAveragePrice', 'MMRAcquisitionAuctionCleanPrice',
                         'MMRAcquisitionRetailAveragePrice', 'MMRAcquisitionRetailCleanPrice',
                         'MMRCurrentAuctionAveragePrice', 'MMRCurrentAuctionCleanPrice', 'MMRCurrentRetailAveragePrice',
                         'MMRCurrentRetailCleanPrice', 'VehBCost', 'WarrantyCost']

    # For numerical columns: replace Nan with the mean of the column
    for col in numerical_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].mean())
        df[col] = df[col].astype('float64')

    return df, numerical_columns, categorical_columns