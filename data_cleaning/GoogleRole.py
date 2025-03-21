import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re
import tldextract
from fake_useragent import UserAgent

# Load dataset
file_path = r"C:\Users\benja\Desktop\Year 3\Sem 2\Text Mining\email_cleaned_with_roles.csv"
df = pd.read_csv(file_path)

# Extract Name & Company from Email
def extract_name(email):
    match = re.match(r"([\w\.]+)@([\w\.]+)", str(email))
    if match:
        name = match.group(1).replace(".", " ").title()
        return name
    return None

def extract_company(email):
    match = re.match(r"([\w\.]+)@([\w\.]+)", str(email))
    if match:
        domain = tldextract.extract(match.group(2))
        return domain.domain.capitalize()
    return None

# Add columns if not already present
if "Sender_Name" not in df.columns:
    df["Sender_Name"] = df["From"].apply(extract_name)
if "Company" not in df.columns:
    df["Company"] = df["From"].apply(extract_company)

# Filter rows where Job_Title is 'Unknown'
unknown_df = df[df["Job_Title"] == "Unknown"]

# Get unique senders only
unique_unknowns = unknown_df[["Sender_Name", "Company", "From"]].dropna().drop_duplicates()

# Google scraping function
def scrape_google_for_role(name, company):
    query = f"{name} {company}"
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": UserAgent().random}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select("div.BNeawe.s3v9rd.AP7Wnd")

        for result in results:
            text = result.get_text()
            match = re.search(r"(CEO|Director|Manager|Analyst|Executive|Consultant|President|Trader|Lawyer|HR|Assistant)", text, re.IGNORECASE)
            if match:
                return match.group(0).title()
        return None
    except Exception as e:
        print(f"Error fetching role for {name} ({company}): {e}")
        return None

# Search and update roles
updated_people = set()

for _, person in unique_unknowns.iterrows():
    name = person["Sender_Name"]
    company = person["Company"]
    sender_email = person["From"]

    if not name or not company:
        continue

    print(f"Searching for {name} ({company})...")
    role = scrape_google_for_role(name, company)

    if role:
        print(f"Found: {role}")
        df.loc[(df["From"] == sender_email) & (df["Job_Title"] == "Unknown"), "Job_Title"] = role
        updated_people.add(sender_email)
    else:
        print("Role not found.")

    time.sleep(3)

# Save updated dataset
output_path = r"C:\Users\benja\Desktop\Year 3\Sem 2\Text Mining\email_cleaned_with_updated_roles.csv"
df.to_csv(output_path, index=False)

print("\nSearch complete.")
print(f"Updated file saved to: {output_path}")
print(f"Total unique senders updated with job titles: {len(updated_people)}")
