# Basimage med Python 3.10
FROM python:3.10.16-slim

# Sätt arbetskatalog
WORKDIR /app

# Uppdatera och installera systemberoenden
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Kopiera requirements.txt till containern
COPY requirements.txt /app/requirements.txt

# Uppdatera pip till den senaste versionen
RUN pip install --upgrade pip

# Installera Python-bibliotek från requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Skapa outputs-mappen (om den inte redan finns)
RUN mkdir -p /app/outputs

# Kopiera DuckDB-filen till outputs-mappen
COPY outputs/hockey_analysis.duckdb /app/outputs/hockey_analysis.duckdb

# Kopiera hela projektet till containern
COPY . .

# Sätt miljövariabel för Docker
ENV DOCKER_ENV=1

# Exponera port 8050 för Dash-applikationen
EXPOSE 8050

# Starta Dash-applikationen
CMD ["python", "dashboard/app.py"]