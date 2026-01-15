import urllib.request
import csv
import io
import math

base_url = "https://raw.githubusercontent.com/MalgorzataOles/GrowthCharts/master/data/"
files = {
    "WHO.Male.BMI.csv": ("erkek", "bmi"),
    "WHO.Female.BMI.csv": ("kiz", "bmi"),
    "WHO.Male.Height.csv": ("erkek", "boy"),
    "WHO.Female.Height.csv": ("kiz", "boy"),
    "WHO.Male.Weight.csv": ("erkek", "kilo"),
    "WHO.Female.Weight.csv": ("kiz", "kilo"),
}

GROWTH_LMS_DATA = {
    'erkek': {'bmi': {}, 'boy': {}, 'kilo': {}},
    'kiz': {'bmi': {}, 'boy': {}, 'kilo': {}}
}

def parse_row(row, type_name):
    # Detect delimiter
    parts = row.split(';')
    if len(parts) < 4:
        parts = row.split(',')
        
    if len(parts) < 4: return None, None, None, None # Header or invalid
    
    try:
        # Age column is usually index 0
        age_val = float(parts[0])
        l = float(parts[1])
        m = float(parts[2])
        s = float(parts[3])
        return age_val, l, m, s
    except ValueError:
        return None, None, None, None

def process_file(filename, gender, metric):
    url = base_url + filename
    print(f"Downloading {filename}...")
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            
        lines = data.strip().split('\n')
        
        # WHO Data Handling:
        # The 'Age' column in these specific CSV files (from MalgorzataOles repo) 
        # is consistently in MONTHS (e.g. 0.0328 months ~ 1 day, 12.0 ~ 1 year).
        # We store them indexed by the nearest integer month.
        
        for line in lines[1:]: # Skip header
            age, l, m, s = parse_row(line, metric)
            if age is None: continue
            
            # Round age to nearest month index
            month_idx = int(round(age))
            
            # Store (overwrite is fine as we want the latest/most precise for that month point if multiple exist)
            GROWTH_LMS_DATA[gender][metric][month_idx] = (l, m, s)
                    
    except Exception as e:
        print(f"Failed to process {filename}: {e}")

print("Starting Data Fetch...")
for fname, (gender, metric) in files.items():
    process_file(fname, gender, metric)

print("Writing growth_data.py...")
with open("growth_data.py", "w", encoding="utf-8") as f:
    f.write("# WHO Child Growth Standards & Reference 2007 (LMS Data)\n")
    f.write("# Generated automatically on user request\n")
    f.write("# Structure: month_index: (L, M, S)\n\n")
    f.write("LMS_DATA = " + str(GROWTH_LMS_DATA))

print("Done! growth_data.py created.")
