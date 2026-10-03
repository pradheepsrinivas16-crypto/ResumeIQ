import pandas as pd
import os
from sklearn.model_selection import train_test_split

# Load cleaned dataset
df = pd.read_csv("data/processed/resume_clean.csv")

print("Total resumes:", len(df))

# First split: 70% training, 30% temporary
train_df, temp_df = train_test_split(
    df,
    test_size=0.30,
    random_state=42,
    stratify=df["Category"]
)

# Second split: temporary 30% into 15% validation and 15% test
val_df, test_df = train_test_split(
    temp_df,
    test_size=0.50,
    random_state=42,
    stratify=temp_df["Category"]
)

# Create output directory
os.makedirs("data/processed", exist_ok=True)

# Save datasets
train_df.to_csv("data/processed/train.csv", index=False)
val_df.to_csv("data/processed/validation.csv", index=False)
test_df.to_csv("data/processed/test.csv", index=False)

# Display results
print("\n========== DATA SPLIT COMPLETE ==========")

print("Training samples:", len(train_df))
print("Validation samples:", len(val_df))
print("Test samples:", len(test_df))

print("\nTotal:", len(train_df) + len(val_df) + len(test_df))

print("\nFiles saved:")
print("data/processed/train.csv")
print("data/processed/validation.csv")
print("data/processed/test.csv")

# Check category distribution
print("\nTraining category distribution:")
print(train_df["Category"].value_counts())