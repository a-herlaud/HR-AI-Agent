import pandas as pd
import Levenshtein
import json
from collections import defaultdict

month_list = [
    "Janvier",
    "Février",
    "Mars",
    "Avril",
    "Mai",
    "Juin",
    "Juillet",
    "Août",
    "Septembre",
    "Octobre",
    "Novembre",
    "Décembre"
]

data = {   
}

def correct_month(word):
    distances = {
        month: Levenshtein.distance(word.lower(), month)
        for month in month_list
    }
    close_month = min(distances, key=distances.get)
    if distances[close_month] < 3:
        return close_month
    return word

def quarter_finder(column_list):
    if "Janvier" in column_list:
        return "Q1"
    if "Février" in column_list:
        return "Q2"
    if "Juillet" in column_list:
        return "Q3"
    if "Octobre" in column_list:
        return "Q4"
    else:
        return None

# def global_quarter(df):


sheets = pd.read_excel("./doc/kpi_rh.xlsx", sheet_name=None, header=2)

def clean_sheet(df):
    for column in df.columns[2:]:
        month = correct_month(column)
        if month != column:
            df = df.rename(columns={column: month})
        if month in month_list or month == "Quarter":
            df[month] = pd.to_numeric(df[month], errors='coerce').astype("Int64")
    df = df.rename(columns={"Total du trimestre": "Quarter"})
    df = df[[col for col in df.columns if col == "KPI" or col == "Quarter" or col in month_list]].dropna()
    df = df.set_index("KPI")

    return df


result = {}
total = defaultdict(lambda: defaultdict(int))
for name, sheet in sheets.items():
    kpis_by_period = clean_sheet(sheet).T.to_dict(orient="index")
    result[name] = {
        period: {
            "kpis": values,
            "analysis": ""
        }
        for period, values in kpis_by_period.items()
    }

    for period, values in kpis_by_period.items():
        for kpi, value in values.items():
            total[period][kpi] += value

result[quarter_finder(clean_sheet(sheets["Pauline"]).columns)] = {
    period: {
        "kpis": dict(values),
        "analysis": ""
    }
    for period, values in total.items()
}
# print(result)

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

# print(sheets)