import os
from typing import Any, Tuple
from prefect import task, flow
from prefect.states import Completed, Failed
from prefect.logging import get_run_logger
from prefect.cache_policies import TASK_SOURCE, INPUTS
from datetime import datetime
from transforms.transform_date import transform_date
from transforms.transform_item import transform_item
from transforms.transform_vendor import transform_vendor

def format_inventory_row(row: list[Any]) -> Tuple[list, list, list]:
    fact_inventory_row = []
    raw_date_row = []
    raw_item_row = []

    # date_id
    date = datetime.strptime(row[0], "%Y-%m-%d")
    raw_date_row.append(date)
    fact_inventory_row.append(None)

    # item_id
    raw_item_row.extend(row[1:4])
    fact_inventory_row.append(row[1])

    fact_inventory_row.append(float(row[4]))  # current_stock
    fact_inventory_row.append(float(row[5]))  # min_required
    fact_inventory_row.append(float(row[6]))  # max_capacity
    fact_inventory_row.append(float(row[7]))  # unit_cost
    fact_inventory_row.append(float(row[8]))  # avg_usage_per_day
    fact_inventory_row.append(float(row[9]))  # restock_lead_time
    fact_inventory_row.append(row[10])  # vendor_id

    return fact_inventory_row, raw_date_row, raw_item_row


@task
def format_inventory(raw_tables: dict[str, dict[str, Any]]) -> Tuple[dict, list, list]:
    fact_inventory = {"name": "fact_inventory",
                      "fields": ["date_id",
                                 "item_id",
                                 "current_stock",
                                 "min_required",
                                 "max_capacity",
                                 "unit_cost",
                                 "avg_usage_per_day",
                                 "restock_lead_time",
                                 "vendor_id"],
                      "rows": []}
    if "inventory_data.csv" not in raw_tables:
        raise Exception("Source table not found")  # type: ignore
    date_rows = []
    item_rows = []

    logger = get_run_logger()
    for i, raw_row in enumerate(raw_tables["inventory_data.csv"]["rows"]):
        try:
            fact_inventory_row, raw_date_row, raw_item_row = format_inventory_row(
                raw_row)
            date_rows.append(raw_date_row)
            item_rows.append(raw_item_row)
            fact_inventory["rows"].append(fact_inventory_row)
        except Exception as e:
            logger.error(f"FORMAT ERROR on row {i}: {e}")
    return fact_inventory, date_rows, item_rows


@task
def bind_inventory(fact_inventory: dict[str, Any], dim_date: dict[str, Any]) -> dict:
    for i, row in enumerate(dim_date["rows"]):
        fact_inventory["rows"][i][0] = i + 1
    return fact_inventory


@flow
def transform_inventory(raw_tables: dict[str, dict[str, Any]]) -> dict:
    fact_inventory, date_rows, item_rows = format_inventory(raw_tables)
    dim_date = transform_date(date_rows)
    dim_item = transform_item(item_rows)
    dim_vendor = transform_vendor(raw_tables)
    fact_inventory = bind_inventory(fact_inventory, dim_date["dim_date"])
    
    fmt_tables = {}
    fmt_tables.update(dim_date)
    fmt_tables.update(dim_item)
    fmt_tables.update(dim_vendor)
    fmt_tables.update({"fact_inventory": fact_inventory})
    
    return fmt_tables

@task(cache_policy=TASK_SOURCE + INPUTS)
def get_inventory_tables(raw_tables: dict[str, dict[str, Any]]) -> dict:
    return transform_inventory(raw_tables)