import os
from typing import Any, Tuple
from prefect import task, flow
from prefect.states import Completed, Failed
from prefect.logging import get_run_logger
from prefect.cache_policies import TASK_SOURCE, INPUTS
from datetime import datetime
from transforms.transform_expense import transform_expense, transform_admission

def format_fact_admission_row(row: list[Any]) -> list:
    fact_admission_row = []

    fact_admission_row.append(None)  # admission_id
    fact_admission_row.append(row[8])  # supplies_used
    fact_admission_row.append(row[9])  # equipment_used
    fact_admission_row.append(row[10])  # nurse_ratio
    fact_admission_row.append(0)  # total_cost

    return fact_admission_row


@task
def format_fact_admission(raw_tables: dict[str, dict[str, Any]]) -> dict:
    fact_admission = {"name": "fact_admission",
                      "fields": ["admission_id",
                                 "supplies_used",
                                 "equipment_used",
                                 "nurse_ratio",
                                 "total_cost"],
                      "rows": []}
    if "admission_data.csv" not in raw_tables:
        raise Exception("Source table not found")  # type: ignore

    logger = get_run_logger()
    for i, raw_row in enumerate(raw_tables["admission_data.csv"]["rows"]):
        try:
            fact_admission_row = format_fact_admission_row(raw_row)
            fact_admission["rows"].append(fact_admission_row)
        except Exception as e:
            logger.error(f"FORMAT ERROR on row {i}: {e}")
    return fact_admission

@task
def bind_fact_admission(fact_admission: dict[str, Any], fact_expense: dict[str, Any]) -> dict:
    for i, row in enumerate(fact_admission["rows"]):
        fact_admission["rows"][i][0] = i + 1
    for i, row in enumerate(fact_expense["rows"]):
        fact_admission["rows"][row[0]-1][4] += row[2]
        
    return fact_admission

@flow
def transform_fact_admission(raw_tables: dict[str, dict[str, Any]]) -> dict:
    fact_admission = format_fact_admission(raw_tables)
    
    fact_expense = transform_expense(raw_tables)
    dim_admission = transform_admission(raw_tables)
    
    fact_admission = bind_fact_admission(fact_admission, fact_expense["fact_expense"])
    
    fmt_tables = {}
    fmt_tables.update(dim_admission)
    fmt_tables.update({"fact_admission": fact_admission})

    return fmt_tables

@task(cache_policy=TASK_SOURCE + INPUTS)
def get_fact_admission_tables(raw_tables: dict[str, dict[str, Any]]) -> dict:
    return transform_fact_admission(raw_tables)