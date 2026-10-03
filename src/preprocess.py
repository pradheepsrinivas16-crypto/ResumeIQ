import pandas as pd
import re
import os

# Load original dataset
df = pd.read_csv("data/raw/Resume.csv")

print("Original dataset:", df.shape)

# Keep only the columns we need
df = df[["Resume_str", "Category"]].copy()


# Clean resume text
def clean_text(text):
    text = str(text)

    # Convert to lowercase
    text = text.lower()

    # Remove extra spaces and new lines
    text = re.sub(r"\s+", " ", text)

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Remove extra spaces again
    text = re.sub(r"\s+", " ", text)

    return text.strip()


df["Resume_str"] = df["Resume_str"].apply(clean_text)

# Remove empty resumes
df = df[df["Resume_str"].str.len() > 0]

# Remove duplicate resumes
df = df.drop_duplicates(subset=["Resume_str"])

# Create processed folder if it doesn't exist
os.makedirs("data/processed", exist_ok=True)

# Save cleaned dataset
output_path = "data/processed/resume_clean.csv"
df.to_csv(output_path, index=False)

print("\n========== PREPROCESSING COMPLETE ==========")
print("Cleaned dataset:", df.shape)
print("Number of categories:", df["Category"].nunique())
print("Saved to:", output_path)

print("\nCategory distribution:")
print(df["Category"].value_counts())