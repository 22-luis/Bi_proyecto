import os
from typing import Any, Tuple, overload
from prefect import task, flow
from prefect.states import Completed, Failed
from prefect.logging import get_run_logger
from prefect.cache_policies import TASK_SOURCE, INPUTS

@task
def format_resource(fmt_rows: list[list[str]]) -> Tuple[dict, list]:
    dim_resource = {"name": "dim_resource",
                "fields": ["resource_name",
                           "resource_category"],
                "rows": []}
    reg_ids: dict[str, int] = {}
    id_bind = []
    logger = get_run_logger()
    
    for i, fmt_row in enumerate(fmt_rows):
        try:
            key = str(fmt_row[0]) + str(fmt_row[1])
            if key in reg_ids:
                id_bind.append(reg_ids[key])
                continue
            reg_ids[key] = len(reg_ids) + 1
            dim_resource["rows"].append(fmt_row)
            id_bind.append(reg_ids[key])
        except Exception as e:
            logger.error(f"FORMAT ERROR on row {i}: {e}")
    return dim_resource, id_bind


@flow
def transform_resource(fmt_rows: list[list[str]]) -> Tuple[dict, list]:
    dim_resource, id_bind = format_resource(fmt_rows)
    return {"dim_resource": dim_resource}, id_bind
