import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

# Load dataset
file_path = r"C:\Users\benja\Downloads\finalv1_data_filtered.csv"
df = pd.read_csv(file_path)

# Filter out rows with known and unknown job titles
known_jobs = df[df['Job_Title'] != 'Unknown']
unknown_jobs = df[df['Job_Title'] == 'Unknown']

# Use Cleaned_Content as input text
X = known_jobs['Cleaned_Content'].fillna('')
y = known_jobs['Job_Title']

# Encode job titles
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split into training and validation
X_train, X_val, y_train, y_val = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Build pipeline: TF-IDF + RandomForest
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=1000, stop_words='english')),
    ("clf", RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train the model
pipeline.fit(X_train, y_train)

# Evaluate
y_pred = pipeline.predict(X_val)
print(classification_report(y_val, y_pred, target_names=le.classes_))

# Predict unknown job titles
X_unknown = unknown_jobs['Cleaned_Content'].fillna('')
unknown_pred = pipeline.predict(X_unknown)
unknown_labels = le.inverse_transform(unknown_pred)

# Assign predictions
unknown_jobs['Predicted_Job_Title'] = unknown_labels

# Combine and save
final_df = pd.concat([known_jobs, unknown_jobs])
final_df.to_csv(r"C:\Users\benja\Downloads\email_with_predicted_roles.csv", index=False)

print("\n Job title prediction complete. Output saved.")
