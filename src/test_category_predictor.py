from resume_parser import extract_resume_text
from category_predictor import predict_category


# -----------------------------------------
# Load resume
# -----------------------------------------

resume_path = "Pradeep_Srinivas_Resume_ATS (1).pdf"  # Change this to your actual resume file

resume_text = extract_resume_text(
    resume_path
)


# -----------------------------------------
# Predict category
# -----------------------------------------

category, confidence = predict_category(
    resume_text
)


# -----------------------------------------
# Display result
# -----------------------------------------

print("\n======================================")
print("       RESUME CATEGORY")
print("======================================")

print("Category:", category)
print(f"Confidence: {confidence:.2f}%")

print("======================================")