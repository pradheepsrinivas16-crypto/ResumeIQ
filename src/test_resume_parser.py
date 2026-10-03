from pathlib import Path
from resume_parser import extract_resume_text


# Find PDF files in the project folder
pdf_files = list(Path(".").glob("*.pdf"))

if not pdf_files:
    print("❌ No PDF found in the project folder.")
    exit()

resume_path = pdf_files[0]

print("Using resume:", resume_path)

text = extract_resume_text(resume_path)

print("=" * 50)
print("RESUME PARSER TEST")
print("=" * 50)

print("Characters:", len(text))
print("Words:", len(text.split()))

print("\nFirst 500 characters:")
print(text[:500])

print("\n✅ Resume parser test successful!")