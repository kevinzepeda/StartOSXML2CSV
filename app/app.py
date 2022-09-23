import os
import requests
import pandas as pd
from io import BytesIO
from typing import List
from dotenv import load_dotenv
from static import reports
from static import types
from static import devices
from pydantic import BaseModel
from requests.auth import HTTPBasicAuth
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse, HTMLResponse


app = FastAPI()
load_dotenv()

class ReportsBase(BaseModel):
    ID: int
    SPGW: str
    IP: str
    URL: str
    ReportType: str
    ReportName: str

class ReportList(BaseModel):
    data: List[ReportsBase]

@app.get("/")
def home():
    page = open('public/index.html','r').read()
    return HTMLResponse(content=page, status_code=200)

@app.get("/reports/")
def getReports():
    return {
        "reports": reports.to_dict('records'),
        "devices": devices,
        "types": types
    }

@app.post("/reports/", response_class=Response)
def reportsByData(data: ReportList):
    files = [getReport(item.URL) for item in data.data]
    dfs = [pd.read_csv(BytesIO(csv)) for csv in files]
    for idx in range(len(dfs)):
        dfs[idx]['SPGW'] = data.data[idx].SPGW
        dfs[idx]['IP'] = data.data[idx].IP
        dfs[idx].name = data.data[idx].ReportType
    types = list(set(pd.DataFrame(data.dict()['data']).ReportType.tolist()))
    sheets = {sheet: pd.concat([df for df in dfs if sheet == df.name]) for sheet in types}
    output = BytesIO()
    writer = pd.ExcelWriter(output,engine='xlsxwriter')
    for idx, sheet in enumerate(types):
        sheets[sheet].to_excel(writer, sheet_name=sheet, index=False)
    writer.save()
    headers = {
        'Content-Disposition': 'attachment; filename="output.xlsx"'
    }
    output.seek(0)
    return StreamingResponse(output, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    

def getReport(url):
    '''
    Get reports from query

    Params
    ------
    url (Str): url to get report

    Return
    ------
    (BytesIO): CSV file form request
    '''
    response = requests.get(url, auth=auth(), verify=False)
    return response.content
    
def auth():
    '''
    Auth Connection
    '''
    return HTTPBasicAuth(os.getenv('CISCO_USER'),os.getenv('CISCO_PASS'))
