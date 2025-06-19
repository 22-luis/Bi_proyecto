import os
from typing import Any, Tuple
from prefect import task, flow
from prefect.states import Completed, Failed
from prefect.logging import get_run_logger
from prefect.cache_policies import TASK_SOURCE, INPUTS
from datetime import datetime
from transforms.transform_staff import transform_staff


def format_staff_shift_row(row: list[Any]) -> Tuple[list, list]:
    fact_staff_shift_row = []
    raw_staff_row = []

    fact_staff_shift_row.append(row[0])  # admission_id
    
    raw_staff_row.extend(row[0:2])
    
    # shift_date
    date1 = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
    fact_staff_shift_row.append(date1.isoformat())
    
    # shift_start_time
    time1 = datetime.strptime(row[3], "%I:%M %p")
    fact_staff_shift_row.append(time1.isoformat())
    
    # shift_end_time
    time2 = datetime.strptime(row[4], "%I:%M %p")
    fact_staff_shift_row.append(time2.isoformat())
    
    fact_staff_shift_row.append(row[5])  # current_assignment
    
    if int(row[6]) < 0:
        raise Exception("hours_worked can't be negative")
    fact_staff_shift_row.append(int(row[6]))  # hours_worked
    if int(row[7]) < 0:
        raise Exception("patients_assigned can't be negative")
    fact_staff_shift_row.append(int(row[7]))  # patients_assigned
    if int(row[8]) < 0:
        raise Exception("overtime_hours can't be negative")
    fact_staff_shift_row.append(int(row[8]))  # overtime_hours

    return fact_staff_shift_row, raw_staff_row


@task
def format_staff_shift(raw_tables: dict[str, dict[str, Any]]) -> Tuple[dict, list]:
    fact_staff_shift = {"name": "fact_staff_shift",
                        "fields": ["staff_id",
                                   "shift_date",
                                   "shift_start_time",
                                   "shift_end_time",
                                   "current_assignment",
                                   "hours_worked",
                                   "patients_assigned",
                                   "overtime_hours"],
                        "rows": []}
    if "staff_shift_data.csv" not in raw_tables:
        raise Exception("Source table not found")  # type: ignore
    staff_rows = []

    logger = get_run_logger()
    for i, raw_row in enumerate(raw_tables["staff_shift_data.csv"]["rows"]):
        try:
            fact_staff_shift_row, raw_resource_row = format_staff_shift_row(
                raw_row)
            staff_rows.append(raw_resource_row)
            fact_staff_shift["rows"].append(fact_staff_shift_row)
        except Exception as e:
            logger.error(f"FORMAT ERROR on row {i}: {e}")
    return fact_staff_shift, staff_rows

@flow
def transform_staff_shift(raw_tables: dict[str, dict[str, Any]]) -> dict:
    fact_staff_shift, staff_rows = format_staff_shift(raw_tables)
    dim_staff = transform_staff(staff_rows)

    fmt_tables = {}
    fmt_tables.update(dim_staff)
    fmt_tables.update({"fact_staff_shift": fact_staff_shift})

    return fmt_tables


@task(cache_policy=TASK_SOURCE + INPUTS)
def get_staff_shift_tables(raw_tables: dict[str, dict[str, Any]]) -> dict:
    return transform_staff_shift(raw_tables)
