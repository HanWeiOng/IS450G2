import pandas as pd
import json

# Load datasets
email_file_path = r"email_cleaned.xlsx - Valid Emails.csv" # Update path using relative path
json_file_path = r"edo_enron-custodians-data.json"  # Update path using relative path


email_df = pd.read_csv(email_file_path)

# Load JSON data
with open(json_file_path, "r", encoding="utf-8") as file:
    enron_data = json.load(file)

# Convert JSON data to DataFrame
enron_roles_df = pd.DataFrame(enron_data)

# 🏷 Select and rename columns
enron_roles_df = enron_roles_df[['email', 'jobTitle']]  # Use correct column names
enron_roles_df.rename(columns={'email': 'From', 'jobTitle': 'Job_Title'}, inplace=True)

# Merge email data with Enron roles
merged_df = email_df.merge(enron_roles_df, how="left", on="From")

# Put Unknown if job title not present
merged_df['Job_Title'].fillna("Unknown", inplace=True)

# Save updated dataset
output_path = r"C:\Users\benja\Downloads\email_cleaned_with_roles.csv"  # Update path
merged_df.to_csv(output_path, index=False)

# Print number of missing roles
missing_roles_df = merged_df[merged_df['Job_Title'] == "Unknown"]
unique_missing_roles = missing_roles_df['From'].nunique()

print(f"\nThere are {unique_missing_roles} unique senders with missing job titles")


print(f"Updated file saved to: {output_path}")

print(f"Total number of rows in the dataset: {len(email_df)}")



