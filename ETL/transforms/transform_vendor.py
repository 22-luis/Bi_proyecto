import os
from typing import Any, Tuple
from prefect import task, flow
from prefect.states import Completed, Failed
from prefect.logging import get_run_logger
from prefect.cache_policies import TASK_SOURCE, INPUTS
from datetime import datetime


def format_vendor_row(row: list[Any]) -> list:
    dim_vendor_row = []

    dim_vendor_row.append(row[0])  # vendor_id
    dim_vendor_row.append(row[1])  # vendor_name
    dim_vendor_row.append(row[2])  # item_supplied
    if int(row[3]) < 0:
        raise Exception("Avg Lead can't be negative")
    dim_vendor_row.append(int(row[3]))  # avg_lead_time_days
    dim_vendor_row.append(float(row[4]))  # cost_per_item

    # last_order_date
    date1 = datetime.strptime(row[5], "%Y-%m-%d")
    dim_vendor_row.append(date1.isoformat())
    # next_delivery_date
    date2 = datetime.strptime(row[6], "%Y-%m-%d")
    dim_vendor_row.append(date2.isoformat())

    return dim_vendor_row


@task
def format_vendor(raw_tables: dict[str, dict[str, Any]]) -> dict:
    dim_vendor = {"name": "dim_vendor",
                  "fields": ["vendor_id",
                             "vendor_name",
                             "item_supplied",
                             "avg_lead_time_days",
                             "cost_per_item",
                             "last_order_date",
                             "next_delivery_date"],
                  "rows": []}
    if "vendor_data.csv" not in raw_tables:
        raise Exception("Source table not found")  # type: ignore

    logger = get_run_logger()
    for i, raw_row in enumerate(raw_tables["vendor_data.csv"]["rows"]):
        try:
            dim_vendor_row = format_vendor_row(raw_row)
            dim_vendor["rows"].append(dim_vendor_row)
        except Exception as e:
            logger.error(f"FORMAT ERROR on row {i}: {e}")
    return dim_vendor


@flow
def transform_vendor(raw_tables: dict[str, dict[str, Any]]) -> dict:
    dim_vendor = format_vendor(raw_tables)

    fmt_tables = {}
    fmt_tables.update({"dim_vendor": dim_vendor})

    return fmt_tables


@task(cache_policy=TASK_SOURCE + INPUTS)
def get_vendor_tables(raw_tables: dict[str, dict[str, Any]]) -> dict:
    return transform_vendor(raw_tables)
