import sqlite3

# Connect to the SQLite database
db_path = "emojis.db"  # Change this to your actual database file path
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Path for the output SQL file
sql_file_path = "main_emojis.sql"

# Open the SQL file for writing
with open(sql_file_path, "w", encoding="utf-8") as f:
    # Write the table creation statement
    f.write("CREATE TABLE IF NOT EXISTS main_emojis (\n")
    f.write("    emoji TEXT,\n")
    f.write("    name TEXT,\n")
    f.write("    `group` TEXT,\n")  # Using backticks to avoid conflicts with reserved keywords
    f.write("    sub_group TEXT,\n")
    f.write("    codepoints TEXT\n")
    f.write(");\n\n")

    # Fetch all data from the main_emojis table
    cursor.execute("SELECT * FROM main_emojis;")
    rows = cursor.fetchall()

    # Generate and write INSERT statements for each row
    for row in rows:
        sanitized_values = []
        for value in row:
            if value is None:
                sanitized_values.append("NULL")  # Handle NULL values properly
            else:
                # Escape single quotes by doubling them
                sanitized_value = str(value).replace("'", "''")
                sanitized_values.append(f"'{sanitized_value}'")

        # Construct and write the INSERT statement
        f.write(f"INSERT INTO main_emojis (emoji, name, `group`, sub_group, codepoints) VALUES ({', '.join(sanitized_values)});\n")

# Close the connection
conn.close()

print(f"SQL file has been created: {sql_file_path}")
