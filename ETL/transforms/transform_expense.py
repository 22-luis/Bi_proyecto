import os
from typing import Any, Tuple
from prefect import task, flow
from prefect.states import Completed, Failed
from prefect.logging import get_run_logger
from prefect.cache_policies import TASK_SOURCE, INPUTS
from datetime import datetime
from transforms.transform_resource import transform_resource
from transforms.transform_admission import transform_admission

def format_expense_row(row: list[Any]) -> Tuple[list, list]:
    fact_expense_row = []
    raw_resource_row = []

    fact_expense_row.append(int(row[0]))  # admission_id
    
    # resource_id
    raw_resource_row.extend(row[2:4])
    fact_expense_row.append(None)
    
    fact_expense_row.append(float(row[4]))  # cost

    return fact_expense_row, raw_resource_row


@task
def format_expense(raw_tables: dict[str, dict[str, Any]]) -> Tuple[dict, list]:
    fact_expense = {"name": "fact_expense",
                   "fields": ["admission_id",
                              "resource_id",
                              "cost"],
                   "rows": []}
    if "expense_data.csv" not in raw_tables:
        raise Exception("Source table not found")  # type: ignore
    resource_rows = []

    logger = get_run_logger()
    for i, raw_row in enumerate(raw_tables["expense_data.csv"]["rows"]):
        try:
            fact_expense_row, raw_resource_row = format_expense_row(raw_row)
            resource_rows.append(raw_resource_row)
            fact_expense["rows"].append(fact_expense_row)
        except Exception as e:
            logger.error(f"FORMAT ERROR on row {i}: {e}")
    return fact_expense, resource_rows


@task
def bind_expense(fact_expense: dict[str, Any], res_id_bind: list[int]) -> dict:
    for i, id in enumerate(res_id_bind):
        fact_expense["rows"][i][1] = id
    return fact_expense


@flow
def transform_expense(raw_tables: dict[str, dict[str, Any]]) -> dict:
    fact_expense, resource_rows = format_expense(raw_tables)
    dim_resource, res_id_bind = transform_resource(resource_rows)
    
    dim_admission = transform_admission(raw_tables)
    fact_expense = bind_expense(fact_expense, res_id_bind)

    fmt_tables = {}
    fmt_tables.update(dim_resource)
    fmt_tables.update(dim_admission)
    fmt_tables.update({"fact_expense": fact_expense})
    
    return fmt_tables

@task(cache_policy=TASK_SOURCE + INPUTS)
def get_expense_tables(raw_tables: dict[str, dict[str, Any]]) -> dict:
    return transform_expense(raw_tables)