import os
from typing import Any, Tuple
from prefect import task, flow
from prefect.states import Completed, Failed
from prefect.logging import get_run_logger
from prefect.cache_policies import TASK_SOURCE, INPUTS
from datetime import datetime
from transforms.transform_admission_type import transform_admission_type
from transforms.transform_medication import transform_medication
from transforms.transform_patient_outcome import transform_patient_outcome
from transforms.transform_patient import transform_patient


def format_admission_row(row: list[Any]) -> Tuple[list, list, list, list]:
    dim_admission_row = []
    raw_admission_type_row = []
    raw_medication_row = []
    raw_patient_outcome_row = []

    dim_admission_row.append(row[0])  # patient_id

    # admission_date
    date1 = datetime.strptime(row[1], "%m/%d/%Y %H:%M")
    dim_admission_row.append(date1.isoformat())

    # discharge_date
    date2 = datetime.strptime(row[2], "%m/%d/%Y %H:%M")
    dim_admission_row.append(date2.isoformat())

    dim_admission_row.append(row[3])  # primary_diagnosis
    dim_admission_row.append(row[5])  # procedure_performed
    dim_admission_row.append(row[6])  # room_type

    if int(row[7]) < 0:
        raise Exception("Bed days can't be negative")
    dim_admission_row.append(int(row[7]))  # bed_days

    #  medication_id
    raw_medication_row.append(row[11])
    dim_admission_row.append(None)

    # admission_type
    raw_admission_type_row.append(row[4])
    dim_admission_row.append(None)

    # patient_outcome_id
    raw_patient_outcome_row.append(row[12])
    dim_admission_row.append(None)
    
    dim_admission_row.append(row[13])
    dim_admission_row.append(row[14])
    dim_admission_row.append(row[15])
    dim_admission_row.append(row[16])
    dim_admission_row.append(row[17])

    return dim_admission_row, raw_admission_type_row, raw_medication_row, raw_patient_outcome_row


@task
def format_admission(raw_tables: dict[str, dict[str, Any]]) -> Tuple[dict, list, list, list]:
    dim_admission = {"name": "dim_admission",
                     "fields": ["patient_id",
                                "admission_date",
                                "discharge_date",
                                "primary_diagnosis",
                                "procedure_performed",
                                "room_type",
                                "bed_days",
                                "medication_id",
                                "admission_type_id",
                                "patient_outcome_id",
                                "registration_time",
                                "triage_time",
                                "medic_time",
                                "total_time",
                                "patient_satisfaction"
],
                     "rows": []}
    if "admission_data.csv" not in raw_tables:
        raise Exception("Source table not found")  # type: ignore
    admission_type_rows = []
    medication_rows = []
    patient_outcome_rows = []

    logger = get_run_logger()
    for i, raw_row in enumerate(raw_tables["admission_data.csv"]["rows"]):
        try:
            dim_admission_row, raw_admission_type_row, raw_medication_row, raw_patient_outcome_row = format_admission_row(
                raw_row)
            admission_type_rows.append(raw_admission_type_row)
            medication_rows.append(raw_medication_row)
            patient_outcome_rows.append(raw_patient_outcome_row)
            dim_admission["rows"].append(dim_admission_row)
        except Exception as e:
            logger.error(f"FORMAT ERROR on row {i}: {e}")
    return dim_admission, admission_type_rows, medication_rows, patient_outcome_rows


@task
def bind_admission(dim_admission: dict[str, Any], med_id_bind: list[int], adm_id_bind: list[int], test_id_bind: list[int]) -> dict:
    for i, id in enumerate(med_id_bind):
        dim_admission["rows"][i][7] = id
    for i, id in enumerate(adm_id_bind):
        dim_admission["rows"][i][8] = id
    for i, id in enumerate(test_id_bind):
        dim_admission["rows"][i][9] = id
    return dim_admission


@flow
def transform_admission(raw_tables: dict[str, dict[str, Any]]) -> dict:
    dim_admission, admission_type_rows, medication_rows, patient_outcome_rows = format_admission(raw_tables)
    
    dim_patient = transform_patient(raw_tables)
    
    dim_medication, med_id_bind = transform_medication(medication_rows)
    dim_admission_type, adm_id_bind = transform_admission_type(admission_type_rows)
    dim_patient_outcome, test_id_bind = transform_patient_outcome(patient_outcome_rows)
    
    dim_admission = bind_admission(dim_admission, med_id_bind, adm_id_bind, test_id_bind)

    fmt_tables = {}
    fmt_tables.update(dim_patient)
    fmt_tables.update(dim_medication)
    fmt_tables.update(dim_admission_type)
    fmt_tables.update(dim_patient_outcome)
    fmt_tables.update({"dim_admission": dim_admission})
    
    return fmt_tables

@task(cache_policy=TASK_SOURCE + INPUTS)
def get_admission_tables(raw_tables: dict[str, dict[str, Any]]) -> dict:
    return transform_admission(raw_tables)