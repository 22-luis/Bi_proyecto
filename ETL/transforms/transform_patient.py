import os
from typing import Any, Tuple
from prefect import task, flow
from prefect.states import Completed, Failed
from prefect.logging import get_run_logger
from prefect.cache_policies import TASK_SOURCE, INPUTS
from datetime import datetime


def format_patient_row(row: list[Any]) -> list:
    dim_patient_row = []

    dim_patient_row.append(row[0])  # patient_id
    dim_patient_row.append(row[1].title())  # name
    if int(row[2]) < 0:
        raise Exception("Age can't be negative")
    dim_patient_row.append(int(row[2]))  # age
    dim_patient_row.append(row[3])  # gender
    dim_patient_row.append(row[4])  # blood_type
    dim_patient_row.append(row[5])  # medical_condition

    return dim_patient_row


@task
def format_patient(raw_tables: dict[str, dict[str, Any]]) -> dict:
    dim_patient = {"name": "dim_patient",
                   "fields": ["patient_id",
                              "name",
                              "age",
                              "gender",
                              "blood_type",
                              "medical_condition"],
                   "rows": []}
    if "patient_data.csv" not in raw_tables:
        raise Exception("Source table not found")  # type: ignore

    logger = get_run_logger()
    for i, raw_row in enumerate(raw_tables["patient_data.csv"]["rows"]):
        try:
            dim_patient_row = format_patient_row(raw_row)
            dim_patient["rows"].append(dim_patient_row)
        except Exception as e:
            logger.error(f"FORMAT ERROR on row {i}: {e}")
    return dim_patient

@flow
def transform_patient(raw_tables: dict[str, dict[str, Any]]) -> dict:
    dim_patient = format_patient(raw_tables)

    fmt_tables = {}
    fmt_tables.update({"dim_patient": dim_patient})

    return fmt_tables

@task(cache_policy=TASK_SOURCE + INPUTS)
def get_patient_tables(raw_tables: dict[str, dict[str, Any]]) -> dict:
    return transform_patient(raw_tables)