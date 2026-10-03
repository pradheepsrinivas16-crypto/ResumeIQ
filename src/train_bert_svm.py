import pandas as pd
import joblib

from sentence_transformers import SentenceTransformer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report


# -----------------------------------------
# 1. Load datasets
# -----------------------------------------

train_df = pd.read_csv("data/processed/train.csv")
val_df = pd.read_csv("data/processed/validation.csv")
test_df = pd.read_csv("data/processed/test.csv")

print("Datasets loaded successfully!")
print("Train:", len(train_df))
print("Validation:", len(val_df))
print("Test:", len(test_df))


# -----------------------------------------
# 2. Get resume text and labels
# -----------------------------------------

X_train = train_df["Resume_str"].fillna("").tolist()
y_train = train_df["Category"]

X_val = val_df["Resume_str"].fillna("").tolist()
y_val = val_df["Category"]

X_test = test_df["Resume_str"].fillna("").tolist()
y_test = test_df["Category"]


# -----------------------------------------
# 3. Load Sentence Transformer
# -----------------------------------------

print("\nLoading Sentence Transformer model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully!")


# -----------------------------------------
# 4. Convert resumes into embeddings
# -----------------------------------------

print("\nCreating training embeddings...")

X_train_embeddings = model.encode(
    X_train,
    batch_size=32,
    show_progress_bar=True
)

print("\nCreating validation embeddings...")

X_val_embeddings = model.encode(
    X_val,
    batch_size=32,
    show_progress_bar=True
)

print("\nCreating test embeddings...")

X_test_embeddings = model.encode(
    X_test,
    batch_size=32,
    show_progress_bar=True
)


# -----------------------------------------
# 5. Train SVM
# -----------------------------------------

print("\nTraining SVM classifier...")

svm_model = LinearSVC()

svm_model.fit(X_train_embeddings, y_train)

print("SVM training completed!")


# -----------------------------------------
# 6. Validation evaluation
# -----------------------------------------

print("\nEvaluating validation set...")

val_predictions = svm_model.predict(X_val_embeddings)

val_accuracy = accuracy_score(y_val, val_predictions)

print(f"Validation Accuracy: {val_accuracy * 100:.2f}%")


# -----------------------------------------
# 7. Test evaluation
# -----------------------------------------

print("\nEvaluating test set...")

test_predictions = svm_model.predict(X_test_embeddings)

test_accuracy = accuracy_score(y_test, test_predictions)

print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, test_predictions, zero_division=0))


# -----------------------------------------
# 8. Save SVM model
# -----------------------------------------

joblib.dump(
    svm_model,
    "models/bert_svm.pkl"
)

print("\nModel saved:")
print("models/bert_svm.pkl")


print("\n======================================")
print("Sentence-BERT + SVM experiment done!")
print("======================================")