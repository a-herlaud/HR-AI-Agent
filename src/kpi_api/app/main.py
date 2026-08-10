from typing import Any
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import json
from create_tables import engine, Kpi
import shutil
import os
from build_kpi_dataframe import build_kpi_dataframe
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel, ConfigDict

app = FastAPI()


class KpiResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    month: str

    nb_candidats_contactes: int
    nb_entretiens_candidats_salaries: int
    nb_entretiens_candidats_sous_traitants: int
    nb_candidats_recrutes_salaries: int
    nb_candidats_integres_sous_traitants: int
    nombre_presentations_clients: int
    nb_refus_cdi_salaries: int
    nombre_ko_candidat_presentation_client: int
    nombre_ko_client_presentation_client: int

# GET GLOBAL KPI FOR THE QUARTER
@app.get("/api/kpis", response_model=list[KpiResponse])
def get_kpis():
    with Session(engine) as session:
        return session.scalars(
            select(Kpi).where(Kpi.month == "Quarter")
        ).all()


# GET GLOBAL KPI FOR A MONTH
@app.get("/api/months/{month}", response_model=list[KpiResponse])
def get_month_kpi(month: str) -> dict[str, Any]:
    with Session(engine) as session:
        return session.scalars(
            select(Kpi).where(Kpi.month == month)
        ).all()

# GET KPI FOR AN EMPLOYEE
@app.get("/api/employees/{name}", response_model=list[KpiResponse])
def get_month_kpi(name: str) -> dict[str, Any]:
    with Session(engine) as session:
        return session.scalars(
            select(Kpi).where(Kpi.name == name)
        ).all()


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
    