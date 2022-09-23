import sys
import os
import pandas as pd
from datetime import datetime

def merge(files):
    '''
    Merge Reports

    Params
    ------

    files (List): List of files to merge

    Return
    ------
    <output_file.xlsx> Excel file with merge
    '''
    Project = 'SEAGW_Reports-'
    Author = 'Kevin_Zepeda-'
    Version = 'v1.0-'
    date = datetime.today()
    date = date.strftime("%d%m%Y")


    files = [filename for filename in files if 'ID-Report_Name' not in filename]
    types = []
    for s in files:
        rType = s[s.find('StarOS'):s.find('\r')]
        if rType not in types and rType != '':
            types.append(rType)
    dataframes = [pd.read_csv(filename) for filename in files]
    for idx,value in enumerate(files):
        dataframes[idx].name = value
        dataframes[idx]['SPGW'] = value[value.find('\r-'):-4][2:]
        
    sheets = {rType: pd.concat([dataframe for dataframe in dataframes if rType in dataframe.name]) for rType in types}

    writer = pd.ExcelWriter(Project + Author + Version + date + '.xlsx',engine='xlsxwriter')   

    for idx, rType in enumerate(types):
        sheets[rType].to_excel(writer,sheet_name=str(rType[:30]),index=False)
    writer.save()

def printHelp():
    print('''
    Merge Reports

    Usage: python merge.py [Files]
    
    Params
    ------
    [Files]: List of files to merge, acept wildcards
        example: reports/*.csv

    Return
    ------
    <file.xlsx>: output file
    ''')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        checkFiles = [os.path.exists(filename) for filename in sys.argv[1:]]
        if all(checkFiles):
            merge(sys.argv[1:])
        else:
            printHelp()
    else:
        printHelp()