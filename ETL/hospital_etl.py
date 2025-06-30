from typing import Any
from prefect import task, flow
from prefect.futures import wait

import table_config
from extract_csv import scan_directory, parse_csv
from transforms.transform_inventory import transform_inventory
from transforms.transform_expense import transform_expense
from transforms.transform_fact_admission import transform_fact_admission
from transforms.transform_staff_shift import transform_staff_shift
from load_sql_server import connect, clear, load



@task()
def print_tables(tables: list[dict[str, Any]]) -> None:
    for table in tables:
        print("\n" + table["name"])
        print(*table["fields"], sep=" | ")
        print(*table["rows"][0], sep=" | ")

@flow
def etl() -> None:

    # Extract
    filePaths = scan_directory(table_config.TABLE_DIR, table_config.CSV_TABLES)
    raw_tables = parse_csv.map(filePaths)
    wait(raw_tables)
    tagged_tables = {}
    for table in raw_tables.result(): tagged_tables[table["name"]] = table 
    
    # Transform
    load_tables = {}
    inventory_state = transform_inventory(tagged_tables, return_state=True)
    if inventory_state.is_completed(): load_tables.update(inventory_state.result())
    expense_state = transform_expense(tagged_tables, return_state=True)
    if expense_state.is_completed(): load_tables.update(expense_state.result())
    admission_state = transform_fact_admission(tagged_tables, return_state=True)
    if admission_state.is_completed(): load_tables.update(admission_state.result())
    staff_shift_state = transform_staff_shift(tagged_tables, return_state=True)
    if staff_shift_state.is_completed(): load_tables.update(staff_shift_state.result())

    # Load
    connection = connect(table_config.CONN_STR)
    for key in load_tables:
        clear(connection, load_tables[key])
    for key in load_tables:
        load(connection, load_tables[key])
        


if __name__ == "__main__":
    etl()
