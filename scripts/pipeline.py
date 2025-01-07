import os
import pandas as pd
import duckdb
import re


def extract_year_from_filename(filename):
    """
    Extract the year from the filename using a regular expression.
    Example: "Metal Ligaen Teams 2022.xlsx" -> 2022
    """
    match = re.search(r'\b(20\d{2})\b', filename)
    return int(match.group(1)) if match else None


def convert_time_on_ice_to_seconds(data, column_name):
    """
    Convert a 'mm:ss' formatted time column to total seconds.
    """
    if column_name in data.columns:
        try:
            # Convert 'mm:ss' to total seconds
            data[column_name] = data[column_name].apply(
                lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]) if pd.notnull(x) else None
            )
            print(f"Converted '{column_name}' to total seconds")
        except Exception as e:
            print(f"Error converting '{column_name}' to seconds: {e}")
    return data


def load_and_combine_excel_files_with_year(directory, sheet_name=None):
    """
    Dynamically load and combine all Excel files in a directory, adding a filename and year column.
    """
    combined_data = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".xlsx", ".xls")):
                file_path = os.path.join(root, file)
                try:
                    year = extract_year_from_filename(file)
                    print(f"Processing file: {file_path}, Year: {year}")
                    
                    # Load Excel file
                    excel_file = pd.ExcelFile(file_path)
                    if sheet_name and sheet_name in excel_file.sheet_names:
                        data = pd.read_excel(file_path, sheet_name=sheet_name)
                    else:
                        print(f"Sheet '{sheet_name}' not found in {file}. Using the first available sheet.")
                        data = pd.read_excel(file_path, sheet_name=0)
                    
                    # Add metadata
                    data['filename'] = file
                    data['year'] = year
                    
                    # Convert 'Time on ice' to total seconds for 'dk_metal_players'
                    if sheet_name == "Box score":
                        data = convert_time_on_ice_to_seconds(data, 'Time on ice')
                    
                    combined_data.append(data)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    if combined_data:
        return pd.concat(combined_data, ignore_index=True)
    else:
        print(f"No Excel files found in the directory: {directory}")
        return pd.DataFrame()


def enforce_column_types(data, column_type_mapping):
    """
    Enforce specific column types based on a provided mapping.
    """
    for column, dtype in column_type_mapping.items():
        if column in data.columns:
            try:
                if dtype == "DATE":
                    # Convert to DATE format
                    data[column] = pd.to_datetime(data[column], errors='coerce').dt.date
                    print(f"Converted column '{column}' to DATE format")
                else:
                    data[column] = data[column].astype(dtype)
                    print(f"Converted column '{column}' to {dtype}")
            except Exception as e:
                print(f"Error converting column '{column}' to {dtype}: {e}")
    return data


def save_to_duckdb(data, db_path, table_name, column_type_mapping=None):
    """
    Save the data to a DuckDB database, optionally enforcing specific column types.
    """
    if not data.empty:
        print(f"Data being saved to DuckDB for table {table_name}:")
        print(data.head())  # Debugging: Display the data being saved

        conn = duckdb.connect(db_path)

        if column_type_mapping:
            data = enforce_column_types(data, column_type_mapping)

        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM data")
        conn.close()
        print(f"Data saved to DuckDB table: {table_name}")
    else:
        print(f"No data to save for table: {table_name}.")


def load_and_save_csv_to_duckdb(directory, db_path, table_name, column_type_mapping=None):
    """
    Load all CSV files from a directory and save them as a table in DuckDB,
    with optional column type enforcement.
    """
    conn = duckdb.connect(db_path)

    try:
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory does not exist: {directory}")

        csv_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".csv")]

        if not csv_files:
            print(f"No CSV files found in directory: {directory}")
            return

        for csv_file in csv_files:
            print(f"Processing CSV file: {csv_file}")
            try:
                # Test both delimiters ';' and ',' dynamically
                try:
                    data = pd.read_csv(csv_file, delimiter=";", header=0, engine="python")
                except Exception:
                    data = pd.read_csv(csv_file, delimiter=",", header=0, engine="python")

                if column_type_mapping:
                    data = enforce_column_types(data, column_type_mapping)

                save_to_duckdb(data, db_path, table_name)

            except Exception as e:
                print(f"Error processing CSV file {csv_file}: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    # Base paths
    script_directory = os.path.dirname(os.path.abspath(__file__))
    base_directory = os.path.abspath(os.path.join(script_directory, ".."))
    db_path = os.path.join(base_directory, "outputs/hockey_analysis.duckdb")

    # Column type mappings
    column_type_mappings = {
        "dk_metal_league": {
            "team": str,
            "points": int,
            "year": int,
            "filename": str
        },
        "dk_metal_games": {
            "team": str,
            "goals": int,
            "Date": "DATE"  # Convert 'Date' column to DATE
        },
        "dk_metal_league_ep": {
            "id": int,
            "name": str,
            "year": int,
            "date": "DATE",
            "league": str
        },
        "dk_metal_players": {
            "player_name": str,
            "team": str,
            "goals": int,
            "assists": int,
            "year": int,
            "Time on ice": int,  # Converted to total seconds
            "filename": str
        },
        "dk_metal_players_ep": {
            "id": int,
            "player_name": str,
            "team": str,
            "points": int,
            "year": int
        }
    }

    # Process Excel files
    table_config = {
        "dk_metal_league": {
            "directory": "data/leagues/dk/dk_metal_league",
            "sheet_name": "Box score - Game total"
        },
        "dk_metal_games": {
            "directory": "data/leagues/dk/dk_metal_games",
            "sheet_name": "Box score"
        },
        "dk_metal_players": {
            "directory": "data/leagues/dk/dk_metal_players",
            "sheet_name": "Box score"
        },
    }

    for table_name, config in table_config.items():
        directory = os.path.join(base_directory, config["directory"])
        sheet_name = config["sheet_name"]

        print(f"Processing data for table: {table_name} from directory: {directory}")
        combined_data = load_and_combine_excel_files_with_year(directory, sheet_name)

        column_mapping = column_type_mappings.get(table_name, None)
        save_to_duckdb(combined_data, db_path, table_name, column_mapping)

    # Process CSV files
    csv_config = {
        "dk_metal_league_ep": {
            "directory": "data/leagues/dk/dk_metal_league_ep"
        },
        "dk_metal_players_ep": {
            "directory": "data/leagues/dk/dk_metal_players_ep"
        },
    }

    for table_name, config in csv_config.items():
        directory = os.path.join(base_directory, config["directory"])
        print(f"Processing CSV files for table: {table_name} from directory: {directory}")

        column_mapping = column_type_mappings.get(table_name, None)
        load_and_save_csv_to_duckdb(directory, db_path, table_name, column_mapping)