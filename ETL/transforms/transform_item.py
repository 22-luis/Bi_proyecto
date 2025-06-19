import os
from typing import Any, Tuple, overload
from prefect import task, flow
from prefect.states import Completed, Failed
from prefect.logging import get_run_logger
from prefect.cache_policies import TASK_SOURCE, INPUTS

@task
def format_item(fmt_rows: list[list[str]]) -> dict:
    dim_item = {"name": "dim_item",
                "fields": ["item_id",
                           "item_type",
                           "item_name"],
                "rows": []}
    reg_ids: dict[str, bool] = {}
    logger = get_run_logger()
    for i, fmt_row in enumerate(fmt_rows):
        try:
            if fmt_row[0] in reg_ids: continue
            reg_ids[fmt_row[0]] = True
            dim_item["rows"].append(fmt_row)
        except Exception as e:
            logger.error(f"FORMAT ERROR on row {i}: {e}")
    return dim_item


@flow
def transform_item(fmt_rows: list[list[str]]) -> dict:
    dim_item = format_item(fmt_rows)
    return {"dim_item": dim_item}
