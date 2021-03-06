"""Write dataframes to files."""
import analysis

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

costCodes = {
    1: 'Material',
    2: 'Labor',
    3: 'Equipment',
    4: 'Subcontractors',
    5: 'Other',
    6: 'Ready Mix'
}


def getMaxOrMinCost(df, isMax):
    """Return max or min cost."""
    index = df['Cost'].idxmax() if isMax else df['Cost'].idxmin()
    return df.loc[index]


def cashFormat(num):
    """Convert number to cash format."""
    return '${:,.2f}'.format(num)


def percentageFormat(num):
    """Convert number to percentage format."""
    return round(num * 100, 2)


def maxOrMinText(df, isMax):
    """Write line of text for max or min cost of dataframe."""
    row = getMaxOrMinCost(df, isMax)
    typeOfCost = 'highest' if isMax else 'lowest'
    return ('The ' + typeOfCost + ' cost was for ' + row.name
            + ' at ' + str(cashFormat(row['Cost'])) + ' which equals '
            + str(percentageFormat(row['Cost %'])) + '% of total costs')


def secondMaxOrMinType(df, isMax):
    """Get second highest max or second lowest min of dataframe."""
    newDF = df.groupby(['Cost Type'])['Cost'].sum()
    type = (newDF.nlargest(2).idxmin(axis=0)
            if isMax else newDF.nsmallest(2).idxmax(axis=0))
    val = newDF[type]
    totalCost = df['Cost'].sum()
    percentage = val / totalCost
    typeOfVal = 'highest' if isMax else 'lowest'
    return ('The second ' + typeOfVal + ' cost was ' + type + ' at '
            + str(cashFormat(val)) + ' which equals '
            + str(percentageFormat(percentage)) + '% of total costs')


def maxOrMinMonth(df, isMax):
    """Get highest or lowest month."""
    row = getMaxOrMinCost(df, isMax)
    typeOfCost = 'highest' if isMax else 'lowest'
    return ('The ' + typeOfCost + ' cost was for the month of '
            + monthCodes[row.name] + ' at ' + str(cashFormat(row['Cost']))
            + ' which equals ' + str(percentageFormat(row['Cost %']))
            + '% of total costs')


def secondMaxOrMinMonth(df, isMax):
    """Get second highest or second lowest month."""
    newDF = df.groupby(['Month'])['Cost'].sum()
    typeIndex = (newDF.nlargest(2).idxmin(axis=0)
                 if isMax else newDF.nsmallest(2).idxmax(axis=0))
    val = newDF[typeIndex]
    totalCost = df['Cost'].sum()
    percentage = val / totalCost
    typeOfVal = 'highest' if isMax else 'lowest'
    return ('The second ' + typeOfVal + ' month was ' + monthCodes[typeIndex]
            + ' at ' + str(cashFormat(val)) + ' which equals '
            + str(percentageFormat(percentage)) + '% of total costs')


def sumText(df):
    """Return text with sum of costs in dataframe."""
    totalCost = df['Cost'].sum()
    return 'The sum of all costs is ' + str(cashFormat(totalCost))


def avgText(df):
    """Return text with average of costs in dataframe."""
    avgCost = df['Cost'].mean()
    return 'The average of all costs is ' + str(cashFormat(avgCost))


def writeTemplate(df, txt):
    """Write .txt file with summary stats."""
    file = ''
    for line in txt:
        file += line + '\n'
    filename = txt[0].replace(" ", "_")+'__Summary.txt'
    text_file = open(filename, "w")
    text_file.write(file)
    print 'Successfully created ' + filename
    return


def createSummaryStats(df):
    """Write .txt file with summary stats."""
    typeDF = analysis.getCostByType(df)
    monthDF = analysis.getCostByMonth(df)

    typeMax = maxOrMinText(typeDF, True)
    typeMax2 = secondMaxOrMinType(typeDF, True)
    typeMin = maxOrMinText(typeDF, False)
    typeMin2 = secondMaxOrMinType(typeDF, False)
    typeSum = sumText(typeDF)
    typeAvg = avgText(typeDF)

    monthSum = sumText(monthDF)
    monthMax = maxOrMinMonth(monthDF, True)
    monthMax2 = secondMaxOrMinMonth(monthDF, True)
    monthMin = maxOrMinMonth(monthDF, False)
    monthMin2 = secondMaxOrMinMonth(monthDF, False)
    monthAvg = avgText(monthDF)
    costByTypeText = ['Cost By Type', typeSum, typeAvg,
                      typeMax, typeMax2, typeMin, typeMin2]
    costByMonthText = ['Cost By Month', monthSum, monthAvg,
                       monthMax, monthMax2, monthMin, monthMin2]
    plotDF(monthDF, costByMonthText[0])
    plotDF(typeDF, costByTypeText[0])
    writeTemplate(typeDF, costByTypeText)
    writeTemplate(monthDF, costByMonthText)
    return


def plotDF(df, title):
    """Plot out dataframe and write .png."""
    filename = title.replace(" ", "_")+'__Summary.png'
    plot = df['Cost'].plot.bar()
    plot.get_figure().savefig(filename)
    print 'Successfully created ' + filename
    return
