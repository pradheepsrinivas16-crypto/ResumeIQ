import pandas as pd
import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report

# ==========================================
# 1. Load datasets
# ==========================================

train_df = pd.read_csv("data/processed/train.csv")
val_df = pd.read_csv("data/processed/validation.csv")
test_df = pd.read_csv("data/processed/test.csv")

X_train = train_df["Resume_str"]
y_train = train_df["Category"]

X_val = val_df["Resume_str"]
y_val = val_df["Category"]

X_test = test_df["Resume_str"]
y_test = test_df["Category"]

print("Training samples:", len(X_train))
print("Validation samples:", len(X_val))
print("Test samples:", len(X_test))


# ==========================================
# 2. Create TF-IDF
# ==========================================

print("\nCreating TF-IDF features...")

tfidf = TfidfVectorizer(
    max_features=10000,
    stop_words="english",
    ngram_range=(1, 2)
)

X_train_tfidf = tfidf.fit_transform(X_train)

# IMPORTANT:
# Only transform validation and test data.
# Do not fit TF-IDF on them.
X_val_tfidf = tfidf.transform(X_val)
X_test_tfidf = tfidf.transform(X_test)

print("TF-IDF shape:", X_train_tfidf.shape)


# ==========================================
# 3. Train SVM
# ==========================================

print("\nTraining SVM model...")

svm_model = LinearSVC()

svm_model.fit(X_train_tfidf, y_train)

print("SVM training completed!")


# ==========================================
# 4. Validation evaluation
# ==========================================

val_predictions = svm_model.predict(X_val_tfidf)

val_accuracy = accuracy_score(y_val, val_predictions)

print("\n========== VALIDATION RESULTS ==========")
print("Validation Accuracy:", round(val_accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_val, val_predictions))


# ==========================================
# 5. Final test evaluation
# ==========================================

test_predictions = svm_model.predict(X_test_tfidf)

test_accuracy = accuracy_score(y_test, test_predictions)

print("\n========== TEST RESULTS ==========")
print("Test Accuracy:", round(test_accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, test_predictions))


# ==========================================
# 6. Save model
# ==========================================

os.makedirs("models", exist_ok=True)

joblib.dump(tfidf, "models/tfidf_vectorizer.pkl")
joblib.dump(svm_model, "models/tfidf_svm.pkl")

print("\nModels saved:")
print("models/tfidf_vectorizer.pkl")
print("models/tfidf_svm.pkl")