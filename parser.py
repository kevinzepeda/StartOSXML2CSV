import os
import sys
import textfsm
import pandas as pd
from datetime import datetime



def parse(filename, temp):
    """
    Parse xml report StarOS Port Fragments Received Statistics
    Params:
    _______
    filename: Str
            xml file
    template: Str
            Fsm file to get data format
    Return:
    ------
    (File): Output file with csv data.
    """
    name = "StarOS_Port_Fragments_Received_Statistics"
    version="v4.0-"
    author = "Kevin_Zepeda-"
    date = datetime.today()
    date = date.strftime("%d%m%Y")

    template = open(temp)
    input_file = open(filename, encoding='utf-8')
    raw_text_data = input_file.readlines()
    data = []
    flag = 0
    for line in raw_text_data:
        if '<reportDataItem>' in line:
            if flag == 0:
                flag += 1
                data.append(line[:21] + ' CardID' + line[21:])
            elif flag == 1:
                flag += 1
                data.append(line[:21] + ' PortID' + line[21:])
            elif flag == 2:
                flag += 1
                data.append(line[:21] + ' Timestamp' + line[21:])
            elif flag == 3:
                flag += 1
                data.append(line[:21] + ' MaximumRate' + line[21:])
            elif flag == 4:
                flag += 1
                data.append(line[:21] + ' FragmentsRecived' + line[21:])
            elif flag == 5:
                flag += 1
                data.append(line[:21] + ' PacketReassembled' + line[21:])
            elif flag == 6:
                flag = 0
                data.append(line[:21] + ' FragmentsSent' + line[21:])
        else:
            data.append(line)
    raw_text_data = ''.join(data)
    re_table = textfsm.TextFSM(template)
    fsm_data = re_table.ParseText(raw_text_data)
    df = pd.DataFrame(fsm_data, columns=re_table.header)
    df.to_csv(filename + '.csv', index=False)

def print_help():
    print('''
    Parse XML from StarOS Port Fragments Received Statistics

    Usage:   python parse.py <filename> <template>

    Params
    ------
    <filename> : XML file
    <template> : FSM template to parse

    Return
    ------
    <outputfile> : CSV file
    ''')
if __name__ == '__main__':
    breakpoint()
    if len(sys.argv) == 3:
        if os.path.exists(sys.argv[1]) and os.path.exists(sys.argv[2]):
            parse(sys.argv[1],sys.argv[2])
        else:
            print_help()
    else:
        print_help()