import sys
import pandas as pd
import numpy as np
from tabulate import tabulate
import analysis
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

def main(df):
    df1 = analysis.getCostByType(df)
    df2 = analysis.getCostByMonth(df)
    df3 = analysis.getCostByMonthAndType(df)
    createFiles([df1, df2, df3], ['CostByType', 'CostByMonth', 'CostByMonthAndType'])
    return

# 1. Ask for user input
#user_input = raw_input("Input the cost journal file path: ") or 'input.xlsx'
# 2. Clean spreadsheet input
#df0 = cleanSpreadsheet(user_input)
# 3. Run program on cleaned spreadsheet
#main(df0)

def getMaxOrMinCost(df, isMax):
    return df.loc[df['Cost'].idxmax()] if isMax else df.loc[df['Cost'].idxmin()]

def cashFormat(num):
    return '${:,.2f}'.format(num)

def percentageFormat(num):
    return int(num * 100)

testDF = analysis.getCostByType(cleanSpreadsheet('input.xlsx'))

def maxOrMinText(df, isMax):
    row = getMaxOrMinCost(df, isMax)
    typeOfCost = 'highest' if isMax else 'lowest'
    return 'The ' + typeOfCost + ' cost was ' + row.name + ' at ' + str(cashFormat(row['Cost'])) + ' which equals ' + str(percentageFormat(row['Cost %'])) + '% of total costs'

def writeTemplate(df, txt):
    file = ''
    for line in txt:
        file += line + '\n'
    text_file = open("Test.txt", "w")
    text_file.write(file)

maxText = maxOrMinText(testDF, True)
minText = maxOrMinText(testDF, False)

writeTemplate(testDF, [maxText, minText])
