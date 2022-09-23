import pandas as pd
reports = pd.read_csv('static/ReportsUrlsList.csv')
types = list(set(reports.ReportName.tolist()))
devices = list(set(reports.SPGW.tolist()))