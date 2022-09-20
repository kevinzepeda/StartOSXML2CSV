# Parse xml report
StarOS Port Fragments Received Statistics

## Simple Parser xml to csv for StarOS Port Fragments
```   
Parse XML from StarOS Port Fragments Received Statistics

    Usage:   python parse.py <filename> <template>

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
bash extract.sh
```
or 
```
sudo chmod +x extract.sh

./extract.sh
```

## Merge Reports
Merge all reports by type in one Excel File

```
python merge.py reports/*.csv
```
