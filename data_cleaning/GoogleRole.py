import pandas as pd

# Load the filtered dataset
df_filtered = pd.read_csv(r"C:\Users\benja\Downloads\email_with_predicted_roles.csv")

# # Filter rows where Job_Title is 'Unknown' (case-insensitive)
# unknown_jobs = df_filtered[df_filtered['Job_Title'].str.strip().str.lower() == 'unknown']

# # Get unique 'From' email addresses for those rows
# unique_unknown_senders = unknown_jobs['From'].unique()

# # Print the result
# print("Number of unique senders with Job_Title as 'Unknown':", len(unique_unknown_senders))
# print(df_filtered.columns)


# Get unique pairs of From and Job_Title
unique_senders_with_roles = df_filtered[['From', 'Job_Title']].drop_duplicates()

# Print the number of unique pairs
print("Number of unique sender-role pairs:", len(unique_senders_with_roles))

# Show the first 10
print(unique_senders_with_roles.head(10))

