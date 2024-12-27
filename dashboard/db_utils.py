import os
import duckdb

# Function to get a connection to the DuckDB database
def get_connection():
    """
    Returns a connection to the DuckDB database.
    Adjusts the database path based on the runtime environment.
    """
    # Kontrollera om vi kör i Docker genom en miljövariabel
    if os.environ.get("DOCKER_ENV", False):  # Använd en Docker-specifik miljövariabel
        db_path = "/app/outputs/hockey_analysis.duckdb"  # Sökväg i Docker-containern
    else:
        db_path = "/Users/emilkarlsson/Documents/Dev/tha-pipeline/outputs/hockey_analysis.duckdb"  # Lokal sökväg

    return duckdb.connect(db_path)