import os
from typing import Any, Tuple, overload
from prefect import task, flow
from prefect.states import Completed, Failed
from prefect.logging import get_run_logger
from prefect.cache_policies import TASK_SOURCE, INPUTS


@task
def format_staff(fmt_rows: list[list[str]]) -> dict:
    dim_staff = {"name": "dim_staff",
                    "fields": ["staff_id",
                               "staff_type"],
                    "rows": []}
    reg_ids: dict[str, int] = {}
    logger = get_run_logger()

    for i, fmt_row in enumerate(fmt_rows):
        try:
            key = fmt_row[0]
            if key in reg_ids:
                continue
            reg_ids[key] = len(reg_ids) + 1
            dim_staff["rows"].append(fmt_row)
        except Exception as e:
            logger.error(f"FORMAT ERROR on row {i}: {e}")
    return dim_staff


@flow
def transform_staff(fmt_rows: list[list[str]]) -> dict:
    dim_staff = format_staff(fmt_rows)
    return {"dim_staff": dim_staff}
