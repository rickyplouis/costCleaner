import os

outputFiles = ['CostByType__Summary.txt', 'CostByMonth__Summary.txt', 'CostByMonthAndType__Summary.txt', 'output.xlsx']

def removeFiles(listOfFiles):
    return [os.remove(filepath) for filepath in listOfFiles if os.path.exists(filepath)]

removeFiles(outputFiles)
