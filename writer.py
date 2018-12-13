import analysis
import pandas as pd

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

def createTextFiles(df):
    typeDF = analysis.getCostByType(df)
    monthDF = analysis.getCostByMonth(df)

    typeMax = maxOrMinText(typeDF, True)
    typeMin = maxOrMinText(typeDF, False)
    typeSum = sumText(typeDF)
    typeAvg = avgText(typeDF)

    monthSum = sumText(monthDF)
    monthMax = maxOrMinMonth(monthDF, True)
    monthMin = maxOrMinMonth(monthDF, False)
    monthAvg = avgText(monthDF)

    costByTypeText = ['Cost By Type', typeSum, typeAvg, typeMax, typeMin]
    costByMonthText = ['Cost By Month', monthSum, monthAvg, monthMax, monthMin]
    writeTemplate(typeDF, costByTypeText)
    writeTemplate(monthDF, costByMonthText)
