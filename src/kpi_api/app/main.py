from typing import Any
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import json
from create_tables import engine
import shutil
import os
from build_kpi_dataframe import build_kpi_dataframe

app = FastAPI()

# GET GLOBAL KPI FOR THE QUARTER
# @app.get("/api")
# def get_global_kpi() -> dict[str, Any]:
#     return db["Q3"]["Quarter"]


# GET GLOBAL KPI FOR A MONTH
# @app.get("/api/months/{month}")
# def get_month_kpi(month: str) -> dict[str, Any]:
#     return db["Q3"][month]


# POST AN EXCEL TO UPLOAD KPI
@app.post("/api")
async def upload(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    try:
        # Save uploaded file temporarily
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Build KPI dataframe
        kpi_df = build_kpi_dataframe(temp_path)

        # Add KPI dataframe to the kpis table
        kpi_df.to_sql(
            name="kpis",
            con=engine,
            if_exists="append",
            index=False,
        )
        
        # Return inserted rows as JSON
        return JSONResponse(content=kpi_df.to_dict(orient="records"))
    
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    