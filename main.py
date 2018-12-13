import sys
import pandas as pd
import numpy as np
from tabulate import tabulate
import analysis
testPath = 'input.xlsx'

monthCodes = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
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
    return round(num * 100, 2)

def maxOrMinText(df, isMax):
    row = getMaxOrMinCost(df, isMax)
    typeOfCost = 'highest' if isMax else 'lowest'
    return 'The ' + typeOfCost + ' cost was for ' + row.name + ' at ' + str(cashFormat(row['Cost'])) + ' which equals ' + str(percentageFormat(row['Cost %'])) + '% of total costs'

def maxOrMinMonth(df, isMax):
    row = getMaxOrMinCost(df, isMax)
    typeOfCost = 'highest' if isMax else 'lowest'
    return 'The ' + typeOfCost + ' cost was for the month of ' + monthCodes[row.name] + ' at ' + str(cashFormat(row['Cost'])) + ' which equals ' + str(percentageFormat(row['Cost %'])) + '% of total costs'

def sumText(df):
    totalCost = df['Cost'].sum()
    return 'The sum of all costs is ' + str(cashFormat(totalCost))

def avgText(df):
    avgCost = df['Cost'].mean()
    return 'The average of all costs is ' + str(cashFormat(avgCost))

def writeTemplate(df, txt):
    file = ''
    for line in txt:
        file += line + '\n'
    filename = txt[0].replace(" ", "_")+'__Summary.txt'
    text_file = open(filename, "w")
    text_file.write(file)

typeDF = analysis.getCostByType(cleanSpreadsheet('input.xlsx'))
monthDF = analysis.getCostByMonth(cleanSpreadsheet('input.xlsx'))

typeMax = maxOrMinText(typeDF, True)
typeMin = maxOrMinText(typeDF, False)
typeSum = sumText(typeDF)
typeAvg = avgText(typeDF)

monthSum = sumText(monthDF)
monthMax = maxOrMinMonth(monthDF, True)
monthMin = maxOrMinMonth(monthDF, False)

costByTypeText = ['Cost By Type', typeSum, typeAvg, typeMax, typeMin]
costByMonthText = ['Cost By Month', monthSum, monthMax, monthMin]
writeTemplate(typeDF, costByTypeText)
writeTemplate(monthDF, costByMonthText)
