import pandas as pd
from tabulate import tabulate
testPath = 'sampleCostJournal.xlsx'

def cleanSpreadsheet(filepath):
    # import dat
    data = pd.ExcelFile(filepath)
    # create dataframe
    df = data.parse(skiprows=5)
    # drop the following columns
    cleanedDF = df.drop(['Unnamed: 0','Unnamed: 1','Trans#', 'Record#', 'Unnamed: 3', 'Description/Job', 'Vendor/Employee/Equipment', 'Unnamed: 8'], axis=1)
    # drops row if any of the cells are blank
    cleanedDF = cleanedDF.dropna(axis=0, how='any')
    print(cleanedDF)
    return cleanedDF


def convertIndex(df):
    df.index = pd.to_datetime(df['Date'])
    return df

def sortByDate(df):
    sortedDF = df.groupby('Date')
    return sortedDF

def getCostByMonth(df):
    return df.resample('M')['Cost'].sum()

newDF = cleanSpreadsheet(testPath)
newDF = convertIndex(newDF)
print(getCostByMonth(newDF))
