import pandas as pd
costCodes = {
    1: 'Material',
    2: 'Labor',
    3: 'Equipment',
    4: 'Subcontractors',
    5: 'Other',
    6: 'Ready Mix'
}

def createCostPercentageCol(df):
    totalCost = df['Cost'].sum()
    df['Cost %'] = df.apply(lambda x: x.Cost / totalCost, axis=1)
    return df

def getCostByMonth(df):
    newDF = df.groupby([df.index.month])['Cost'].sum()
    newDF.index.rename('Month', inplace=True)
    return createCostPercentageCol(pd.DataFrame(newDF))

def getCostByType(df):
    newDF = df.replace({'Cost Type': costCodes})
    newDF = newDF.groupby(['Cost Type'])['Cost'].sum()
    return createCostPercentageCol(pd.DataFrame(newDF))

def getCostByMonthAndType(df):
    newDF = df.replace({'Cost Type': costCodes})
    newDF = newDF.groupby([df.index.month, 'Cost Type'])['Cost'].sum()
    newDF.index.rename(['Month', 'Cost Type'], inplace=True)
    return newDF
