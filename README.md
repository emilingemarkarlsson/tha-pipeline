
# Projektguide: Tha-Pipeline

## 1. Förberedelser
### 1.1 Installera nödvändiga verktyg
1. **Python**: Installera Python 3.10 via [pyenv](https://github.com/pyenv/pyenv):
   ```bash
   brew update
   brew install pyenv
   pyenv install 3.10.12
   pyenv global 3.10.12
   ```
   Verifiera installationen:
   ```bash
   python --version
   ```

2. **Git**: Installera Git om det inte redan är installerat:
   ```bash
   brew install git
   ```

3. **Visual Studio Code**:
   - Ladda ner och installera [VS Code](https://code.visualstudio.com/).
   - Installera tillägg för Python och GitHub i VS Code.

---

## 2. Skapa och initiera projektet
### 2.1 Skapa projektmappen
1. Navigera till rätt plats och skapa projektmappen:
   ```bash
   cd /Users/emilkarlsson/Documents/Dev
   mkdir tha-pipeline
   cd tha-pipeline
   ```

2. Initiera ett Git-repo:
   ```bash
   git init
   ```

### 2.2 Skapa grundläggande projektstruktur
1. Skapa en mappstruktur:
   ```bash
   mkdir data scripts outputs
   touch README.md requirements.txt .gitignore
   ```

2. Lägg till följande i `.gitignore`:
   ```plaintext
   __pycache__/
   *.pyc
   outputs/
   data/
   ```

---

## 3. Ställ in din Python-miljö
### 3.1 Skapa en virtuell miljö
1. Skapa en virtuell miljö:
   ```bash
   python -m venv venv
   ```

2. Aktivera den:
   ```bash
   source venv/bin/activate
   ```

3. Verifiera att rätt Python-version används:
   ```bash
   python --version
   ```

### 3.2 Installera beroenden
1. Lägg till några initiala paket i `requirements.txt`:
   ```plaintext
   pandas
   numpy
   openpyxl
   duckdb
   rill
   ```

2. Installera beroenden:
   ```bash
   pip install -r requirements.txt
   ```

---

## 4. Skapa din första pipeline
1. Skapa ett skript `scripts/pipeline.py`:
   ```bash
   touch scripts/pipeline.py
   ```

2. Fyll i med följande kod:
   ```python
   import pandas as pd
   import duckdb

   def load_excel(file_path):
       return pd.read_excel(file_path)

   def transform_data(data):
       data['Player'] = data['Player'].str.upper()
       return data

   def save_to_duckdb(data, db_path="outputs/hockey_analysis.duckdb"):
       conn = duckdb.connect(db_path)
       conn.execute("CREATE TABLE IF NOT EXISTS players AS SELECT * FROM data")
       print("Data saved to DuckDB!")

   if __name__ == "__main__":
       # Testa pipelinen med en testfil
       df = load_excel("data/players.xlsx")
       df = transform_data(df)
       save_to_duckdb(df)
   ```

3. Lägg till en test-Excel-fil i `data/players.xlsx`.

4. Kör skriptet:
   ```bash
   python scripts/pipeline.py
   ```

---

## 5. Anslut till GitHub
### 5.1 Skapa ett GitHub-repo
1. Gå till [GitHub](https://github.com/) och skapa ett nytt privat repo med namnet `tha-pipeline`.

2. Anslut ditt lokala repo till GitHub:
   ```bash
   git remote add origin https://github.com/emilkarlsson/tha-pipeline.git
   git branch -M main
   ```

### 5.2 Lägg till och pusha filer
1. Lägg till filer:
   ```bash
   git add .
   git commit -m "Initial commit"
   ```

2. Pusha till GitHub:
   ```bash
   git push -u origin main
   ```

---

## 6. Nästa steg
### 6.1 Lägg till fler funktioner
- Skapa fler pipelines för att hantera webbskrapning och andra datakällor.
- Lägg till stöd för schemaläggning (t.ex. via Cron).

### 6.2 Automatisera och visualisera
- Installera och integrera Rill för att visualisera data från DuckDB:
   ```bash
   rill start outputs/hockey_analysis.duckdb
   ```

### 6.3 Förbered för Docker och produktion
- När projektet växer, bygg en Dockerfile för enkel distribution.
