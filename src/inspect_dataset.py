import pandas as pd

# Load the dataset
df = pd.read_csv("data/raw/Resume.csv")

print("========== DATASET INFORMATION ==========")

# Number of rows and columns
print("Number of resumes:", len(df))
print("Number of columns:", len(df.columns))

# Column names
print("\nColumns:")
print(df.columns.tolist())

# First 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Number of categories
print("\nNumber of categories:", df["Category"].nunique())

# Category distribution
print("\nCategory distribution:")
print(df["Category"].value_counts())

# Missing values
print("\nMissing values:")
print(df.isnull().sum())

# Duplicate rows
print("\nDuplicate rows:", df.duplicated().sum())