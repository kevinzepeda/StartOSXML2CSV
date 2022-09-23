# StarOS Port Fragments Received Statistics
Extract Transform and get data in one file from StartOS

Requeriments:
    - Python3.9
    - pip install -r requeriments.txt

## Server Mode
```

```
## Simple Parser xml to csv for StarOS Port Fragments
```   
Parse XML from StarOS Port Fragments Received Statistics

    Usage:   python app/parse.py <filename> <template>

    Params
    ------
    <filename> : XML file
    <template> : FSM template to parse

    Return
    ------
    <outputfile> : CSV file
```
## Extract and Parse files from csv
All file are saved on `reports` folder if not exists

```
mkdir reports
```

Connect to VPN and then execute:
```
bash app/extract.sh
```
or 
```
sudo chmod +x extract.sh

./extract.sh
```

## Merge Reports
Merge all reports by type in one Excel File

```
python app/merge.py reports/*.csv
```
