import os

outputFiles = ['Cost_By_Type__Summary.txt', 'Cost_By_Month__Summary.txt', 'Cost_By_Month_And_Type__Summary.txt', 'Test.txt', 'output.xlsx']

def removeFiles(listOfFiles):
    print('Successfully removed all output files')
    return [os.remove(filepath) for filepath in listOfFiles if os.path.exists(filepath)]

removeFiles(outputFiles)
