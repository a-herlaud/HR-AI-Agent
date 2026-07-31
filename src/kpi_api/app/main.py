from fastapi import FastAPI
import json

app = FastAPI()

# ADD TO LIFESPAN LATER
with open("./database/output.json", "r") as f:
    db = json.load(f)

# GET GLOBAL KPI FOR THE QUARTER
@app.get("/api")
def get_global_kpi():
    return db["Q3"]["Quarter"]


# GET GLOBAL KPI FOR A MONTH
@app.get("/api/months/{month}")
def get_month_kpi(month: str):
    return db["Q3"][month]



# POST AN EXCEL TO UPLOAD KPI
# app.post()
# def post_quarter_kpi():
#     return {status:ok, response="good"}
    