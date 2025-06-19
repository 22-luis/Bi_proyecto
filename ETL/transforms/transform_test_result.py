import os
from typing import Any, Tuple, overload
from prefect import task, flow
from prefect.states import Completed, Failed
from prefect.logging import get_run_logger
from prefect.cache_policies import TASK_SOURCE, INPUTS

@task
def format_test_result(fmt_rows: list[list[str]]) -> Tuple[dict, list]:
    dim_test_result = {"name": "dim_test_result",
                "fields": ["test_result"],
                "rows": []}
    reg_ids: dict[str, int] = {}
    id_bind = []
    logger = get_run_logger()
    for i, fmt_row in enumerate(fmt_rows):
        try:
            if fmt_row[0] in reg_ids:
                id_bind.append(reg_ids[fmt_row[0]])
                continue
            reg_ids[fmt_row[0]] = len(reg_ids) + 1
            dim_test_result["rows"].append(fmt_row)
            id_bind.append(reg_ids[fmt_row[0]])
        except Exception as e:
            logger.error(f"FORMAT ERROR on row {i}: {e}")
    return dim_test_result, id_bind


@flow
def transform_test_result(fmt_rows: list[list[str]]) -> Tuple[dict, list]:
    dim_test_result, id_bind = format_test_result(fmt_rows)
    return {"dim_test_result": dim_test_result}, id_bind
