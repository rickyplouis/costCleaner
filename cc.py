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

def sortByDate(df):
    sortedDF = df.groupby('Date')
    return sortedDF

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

def writeToExcel(df):
    df0 = cleanSpreadsheet(testPath)
    df1 = getCostByType(df0)
    df2 = getCostByMonth(df0)
    df3 = getCostByMonthAndType(df0)
    writer = pd.ExcelWriter('output.xlsx')
    df1.to_excel(writer, 'CostByType')
    writeStatsToFile(df1, 'CostByType__Summary')
    df2.to_excel(writer, 'CostByMonth')
    print('Successfully created CostByMonth.txt')
    writeStatsToFile(df2, 'CostByMonth__Summary')
    df3.to_excel(writer, 'CostByMonthAndType')
    print('Successfully created CostByMonthAndType.txt')
    writeStatsToFile(df3, 'CostByMonthAndType__Summary')
    print('Successfully created CostByMonthAndType__Summary.txt')
    writer.save()
    print('Successfully created output.xlsx')
    return

df00 = cleanSpreadsheet(testPath)
writeToExcel(df00)
