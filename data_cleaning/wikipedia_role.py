import pandas as pd
import re
import time
import wikipedia

# Load dataset
file_path = r"C:\Users\benja\Downloads\finalv1_data_filtered.csv"
df = pd.read_csv(file_path)

# Extract name from email
def extract_name(email):
    match = re.match(r"([\w\.]+)@([\w\.]+)", str(email))
    if match:
        return match.group(1).replace(".", " ").title()
    return None

# Extract company from domain
def extract_company(email):
    match = re.match(r"[\w\.]+@([\w\-]+)\.", str(email))
    if match:
        return match.group(1).capitalize()
    return None

# Add columns
df["Sender_Name"] = df["From"].apply(extract_name)
df["Company"] = df["From"].apply(extract_company)

# Filter unknown job titles
unknown_df = df[df["Job_Title"] == "Unknown"]
unique_unknowns = unknown_df[["Sender_Name", "Company", "From"]].dropna().drop_duplicates()

# Extract role from summary
def extract_role_flexible(summary, name):
    summary_sentences = re.split(r'(?<=[.!?])\s+', summary)
    for sentence in summary_sentences:
        if 'Enron' in sentence and name.split()[0] in sentence:
            match = re.search(r"(was|served as|became|worked as|held the position of)\s+(.*?)(\.|,|;|$)", sentence, re.IGNORECASE)
            if match:
                return match.group(2).strip()
    return None

# Search Wikipedia
def extract_role_from_wikipedia(name):
    try:
        query = f"{name} Enron"
        results = wikipedia.search(query)
        valid_results = [r for r in results if name.lower() in r.lower() and not r.lower().startswith("list of")]

        if valid_results:
            summary = wikipedia.summary(valid_results[0], sentences=3)
            return extract_role_flexible(summary, name)
        return None
    except Exception:
        return None

# Sample test
sample = unique_unknowns.head(10)
results = []

for _, row in sample.iterrows():
    name = row["Sender_Name"]
    email = row["From"]
    role = extract_role_from_wikipedia(name)
    results.append((name, email, role))

for r in results:
    print(r)
