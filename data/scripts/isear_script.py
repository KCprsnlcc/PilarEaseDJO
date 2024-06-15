import pyodbc

def list_tables(access_db_path):
    conn_str = (
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        rf"DBQ={access_db_path};"
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.tables()
    tables = [row.table_name for row in cursor.fetchall()]
    conn.close()
    return tables

# Provide the correct path to the ISEAR database
isear_db_path = 'C:\\xampp\\htdocs\\PilarEaseDJO\\data\\scripts\\isear_databank.mdb'
tables = list_tables(isear_db_path)
print("Tables in the database:", tables)