import os
import pandas as pd
import duckdb
import re

def extract_year_from_filename(filename):
    """
    Extract the year from the filename using a regular expression.
    Example: "Metal Ligaen Teams 2022.xlsx" -> 2022
    """
    match = re.search(r'\b(20\d{2})\b', filename)  # Matches "2022", "2023", etc.
    return int(match.group(1)) if match else None

def load_and_combine_excel_files_with_year(directory, sheet_name):
    """
    Dynamically load and combine all Excel files in a directory, adding a filename and year column.
    """
    combined_data = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".xlsx", ".xls")):
                file_path = os.path.join(root, file)
                print(f"Found file: {file_path}")
                try:
                    year = extract_year_from_filename(file)
                    print(f"Processing file: {file_path}, Year: {year}")
                    
                    # Load data
                    data = pd.read_excel(file_path, sheet_name=sheet_name)
                    print(f"Columns in {file}: {list(data.columns)}")
                    
                    if not data.empty:
                        # Standardize column names
                        data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_").str.replace(",", "")
                        
                        # Add additional columns
                        data['filename'] = file
                        data['year'] = year
                        combined_data.append(data)
                    else:
                        print(f"No data found in {file_path}, sheet: {sheet_name}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    return pd.concat(combined_data, ignore_index=True) if combined_data else pd.DataFrame()

def inspect_duckdb_table(db_path, table_name):
    """
    Inspect the schema of a DuckDB table.
    """
    conn = duckdb.connect(db_path)
    table_info = conn.execute(f"PRAGMA table_info('{table_name}')").fetchdf()
    conn.close()
    return table_info

def preview_duckdb_table(db_path, table_name, limit=5):
    """
    Preview the first few rows of a DuckDB table.
    """
    conn = duckdb.connect(db_path)
    data = conn.execute(f"SELECT * FROM {table_name} LIMIT {limit}").fetchdf()
    conn.close()
    return data

def save_to_duckdb(data, db_path, table_name, column_types=None):
    """
    Save the combined data to a DuckDB database.
    Drops the existing table and recreates it to match the new schema.
    Optionally adjusts column types.
    """
    if not data.empty:
        conn = duckdb.connect(db_path)
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM data")

        existing_columns = set(data.columns)
        if column_types:
            for column, data_type in column_types.items():
                if column in existing_columns:
                    try:
                        conn.execute(f"ALTER TABLE {table_name} ALTER COLUMN {column} TYPE {data_type}")
                        print(f"Set column '{column}' to type '{data_type}' in table '{table_name}'")
                    except Exception as e:
                        print(f"Error altering column '{column}' in table '{table_name}': {e}")
                else:
                    print(f"Column '{column}' not found in data for table '{table_name}'. Skipping.")
        
        print(f"Schema of table '{table_name}':")
        print(inspect_duckdb_table(db_path, table_name))
        conn.close()
        print(f"Data saved to DuckDB table: {table_name}")
    else:
        print(f"No data to save to DuckDB for table: {table_name}.")

if __name__ == "__main__":
    base_directory = "/Users/emilkarlsson/Documents/Dev/tha-pipeline"
    db_path = os.path.join(base_directory, "outputs/hockey_analysis.duckdb")

    table_config = {
        "dk_metal_league": {
            "directory": "/Users/emilkarlsson/Documents/Dev/tha-pipeline/data/leagues/dk/dk_metal_league",
            "sheet_name": "Box score - Game total",
            "column_types": {
                "year": "INTEGER",
                "filename": "TEXT",
                "team": "TEXT",
                "season": "INTEGER",
                "goals": "INTEGER",
                "penalties": "INTEGER",
                "faceoffs_won_%": "TEXT"
            }
        },
        "dk_metal_games": {
            "directory": "/Users/emilkarlsson/Documents/Dev/tha-pipeline/data/leagues/dk/dk_metal_games",
            "sheet_name": "Box score",
            "column_types": {
                "year": "INTEGER",
                "filename": "TEXT",
                "date": "DATE",
                "season": "INTEGER",
                "opponent": "TEXT",
                "score": "TEXT",
                "goals": "INTEGER",
                "penalties": "INTEGER",
                "faceoffs_won": "INTEGER",
                "entries": "INTEGER"
            }
        },
    }

    for table_name, config in table_config.items():
        directory = config["directory"]
        sheet_name = config["sheet_name"]
        column_types = config.get("column_types", {})

        print(f"Processing data for table: {table_name} from directory: {directory}")
        try:
            files = os.listdir(directory)
            print(f"Files in directory '{directory}': {files}")
        except FileNotFoundError:
            print(f"Directory '{directory}' not found. Skipping.")
            continue

        combined_data = load_and_combine_excel_files_with_year(directory, sheet_name)
        save_to_duckdb(combined_data, db_path, table_name, column_types)
        
        # Preview the first 5 rows of the table
        print(f"Preview of table '{table_name}':")
        print(preview_duckdb_table(db_path, table_name))