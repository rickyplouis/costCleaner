import sys
import pandas as pd
import numpy as np
from tabulate import tabulate
import analysis
import writer
testPath = 'input.xlsx'

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

def createSpreadsheet(listOfDf, listofPaths):
    writer = pd.ExcelWriter('output.xlsx')
    for df, path in zip(listOfDf, listofPaths):
        df.to_excel(writer, path)
    writer.save()
    print('Successfully created output.xlsx')
    return

def main(df):
    df1 = analysis.getCostByType(df)
    df2 = analysis.getCostByMonth(df)
    df3 = analysis.getCostByMonthAndType(df)
    writer.createTextFiles(df)
    createSpreadsheet([df1, df2, df3], ['CostByType', 'CostByMonth', 'CostByMonthAndType'])
    return

# 1. Ask for user input
user_input = raw_input("Input the cost journal file path: ") or 'input.xlsx'
# 2. Clean spreadsheet input
df0 = cleanSpreadsheet(user_input)
# 3. Run program on cleaned spreadsheet
main(df0)
