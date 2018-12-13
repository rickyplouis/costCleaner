import os

outputFiles = [
    'Cost_By_Month__Summary.png',
    'Cost_By_Month__Summary.txt',
    'Cost_By_Type__Summary.txt',
    'Cost_By_Type__Summary.png',
    'Cost_By_Month_And_Type__Summary.txt',
    'Test.txt',
    'output.xlsx'
    ]

def removeFiles(listOfFiles):
    for filepath in listOfFiles:
        if os.path.exists(filepath):
            os.remove(filepath)
            print 'Successfully removed ' + filepath

removeFiles(outputFiles)
