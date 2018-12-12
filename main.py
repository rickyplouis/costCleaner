import sys
import pandas as pd
import numpy as np
from tabulate import tabulate
testPath = 'input.xlsx'

costCodes = {
    1: 'Material',
    2: 'Labor',
    3: 'Equipment',
    4: 'Subcontractors',
    5: 'Other',
    6: 'Ready Mix'
}

def cleanSpreadsheet(filepath):
    # import dat
    data = pd.ExcelFile(filepath)
    # create dataframe
    df = data.parse(skiprows=5)
    # drop the following columns
    cleanedDF = df.drop(['Unnamed: 0','Unnamed: 1','Trans#', 'Record#', 'Unnamed: 3', 'Description/Job', 'Vendor/Employee/Equipment', 'Unnamed: 8'], axis=1)
    # drops row if any of the cells are blank
    cleanedDF = cleanedDF.dropna(axis=0, how='any')
    cleanedDF = convertIndex(cleanedDF)
    return cleanedDF

def convertIndex(df):
    df.index = pd.to_datetime(df['Date'])
    return df

def getCostByMonth(df):
    newDF = df.groupby([df.index.month])['Cost'].sum()
    newDF.index.rename('Month', inplace=True)
    return newDF

def getCostByType(df):
    newDF = df.replace({'Cost Type': costCodes})
    return newDF.groupby(['Cost Type'])['Cost'].sum()

def getCostByMonthAndType(df):
    newDF = df.replace({'Cost Type': costCodes})
    newDF = newDF.groupby([df.index.month, 'Cost Type'])['Cost'].sum()
    newDF.index.rename(['Month', 'Cost Type'], inplace=True)
    return newDF

def writeStatsToFile(df, filename):
    df.describe().to_csv(filename+'.txt', header=False, index=True, sep=' ')
    print('Successfully created'+filename+'.txt')
    return

def createFiles(listOfDf, listofPaths):
    writer = pd.ExcelWriter('output.xlsx')
    for df, path in zip(listOfDf, listofPaths):
        df.to_excel(writer, path)
        writeStatsToFile(df, path+'__Summary')
    writer.save()
    print('Successfully created output.xlsx')
    return

def writer(df):
    df1 = getCostByType(df)
    df2 = getCostByMonth(df)
    df3 = getCostByMonthAndType(df)
    createFiles([df1, df2, df3], ['CostByType', 'CostByMonth', 'CostByMonthAndType'])
    return

# Now ask for input
user_input = raw_input("Input the cost journal file path: ") or 'input.xlsx'

df0 = cleanSpreadsheet(user_input)

writer(df0)
