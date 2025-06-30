TABLE_DIR = "../Base Proyecto/"

CSV_TABLES = [
    "admission_data.csv",
    "expense_data.csv",
    "inventory_data.csv",
    "patient_data.csv",
    "staff_shift_data.csv",
    "vendor_data.csv"
]

DB_NAME = 'DW'

CONN_STR = f'Driver={{ODBC Driver 17 for SQL Server}};Server=.\\TESTDW;Database={DB_NAME};Trusted_Connection=yes;'