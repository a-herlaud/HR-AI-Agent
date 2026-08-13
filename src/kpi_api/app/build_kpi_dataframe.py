import pandas as pd
import Levenshtein

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

def build_kpi_dataframe(excel_path: str = "kpi_rh.xlsx") -> pd.DataFrame:
    sheets = pd.read_excel(excel_path, sheet_name=None, header=2)


    def clean_sheet(df):
        for column in df.columns[2:]:
            month = correct_month(column)
            if month != column:
                df = df.rename(columns={column: month})
            if month in month_list or month == "Quarter":
                df[month] = (
                    pd.to_numeric(df[month], errors="coerce")
                    .fillna(0)
                    .astype("int64")
                )
        df = df.rename(columns={"Total du trimestre": "Quarter"})
        df = df[[col for col in df.columns if col == "KPI" or col == "Quarter" or col in month_list]].dropna()
        df = df.set_index("KPI")

        return df

    rows = []
    total_by_period = {}


    for name, sheet in sheets.items():
        quarter_name = quarter_finder(clean_sheet(sheet).columns)
        kpis_by_period = clean_sheet(sheet).T
        for period, values in kpis_by_period.iterrows():
            row = {"name": name, "quarter": quarter_name, "month": period, **values.to_dict()}
            rows.append(row)

            if period not in total_by_period:
                total_by_period[period] = values.to_dict()
            else:
                for kpi_label in values.index:
                    total_by_period[period][kpi_label] = total_by_period[period].get(kpi_label, 0) + values[kpi_label]

    for period, values in total_by_period.items():
        rows.append({"name": "quarter", "quarter": quarter_name, "month": period, **values})
    return pd.DataFrame(rows)