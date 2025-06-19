import os
from typing import Any, Tuple, overload
from prefect import task, flow
from prefect.states import Completed, Failed
from prefect.logging import get_run_logger
from prefect.cache_policies import TASK_SOURCE, INPUTS
from datetime import datetime
import numbers


def format_date_row(date: datetime) -> list:
    dim_date_row = []

    dim_date_row.append(date.isoformat())  # full_date
    dim_date_row.append(date.day)  # day
    dim_date_row.append(date.month)  # month
    dim_date_row.append(date.year)  # year
    dim_date_row.append((date.month-1)//3+1)  # quarter
    dim_date_row.append(date.weekday())  # day_of_week

    return dim_date_row


@task
def format_date(fmt_rows: list[list[datetime]]) -> dict:
    dim_date = {"name": "dim_date",
                 "fields": ["full_date",
                            "day",
                            "month",
                            "year",
                            "quarter",
                            "day_of_week"],
                 "rows": []}
    logger = get_run_logger()
    for i, fmt_row in enumerate(fmt_rows):
        try:
            dim_date_row = format_date_row(fmt_row[0])
            dim_date["rows"].append(dim_date_row)
        except Exception as e:
            logger.error(f"FORMAT ERROR on row {i}: {e}")
    return dim_date


@flow
def transform_date(fmt_rows: list[list[datetime]]) -> dict:
    dim_date = format_date(fmt_rows)
    return {"dim_date": dim_date}
