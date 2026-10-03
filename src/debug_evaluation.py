import pandas as pd

RESULTS_PATH = "data/evaluation/compatibility_results.csv"
DATASET_PATH = "data/evaluation/compatibility_test_set.csv"

results = pd.read_csv(RESULTS_PATH)
dataset = pd.read_csv(DATASET_PATH)

# Merge evaluation results with original resume/JD text
df = results.merge(
    dataset[["pair_id", "resume_text", "job_description"]],
    on="pair_id",
    how="left"
)

errors = df[df["human_label"] != df["predicted_label"]]

print("\n" + "=" * 70)
print("COMPATIBILITY ERROR ANALYSIS")
print("=" * 70)

print(f"\nTotal pairs   : {len(df)}")
print(f"Correct       : {(df['human_label'] == df['predicted_label']).sum()}")
print(f"Errors        : {len(errors)}")

print("\n" + "-" * 70)
print("WRONG PREDICTIONS")
print("-" * 70)

for _, row in errors.iterrows():

    print(f"""
Pair ID          : {row['pair_id']}
Human Label      : {row['human_label']}
Predicted Label  : {row['predicted_label']}

Semantic Score   : {row['semantic_score']:.2f}
Skill Score      : {row['skill_score']:.2f}
Final Score      : {row['final_score']:.2f}

Resume:
{row['resume_text'][:700]}

Job Description:
{row['job_description'][:700]}

{"-" * 70}
""")