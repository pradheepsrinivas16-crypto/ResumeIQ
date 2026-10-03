from recommendations import generate_recommendations


# ==========================================
# TEST DATA
# ==========================================

matched_skills = [
    "sql",
    "excel",
    "power bi"
]

missing_skills = [
    "tableau",
    "data visualization",
    "statistical analysis"
]


# ==========================================
# GENERATE RECOMMENDATIONS
# ==========================================

result = generate_recommendations(
    matched_skills,
    missing_skills
)


# ==========================================
# DISPLAY RESULT
# ==========================================

print("\n======================================")
print("       RESUME RECOMMENDATIONS")
print("======================================")


print("\n💪 Strengths:")

for strength in result["strengths"]:
    print("✓", strength)


print("\n⚠️ Skill Gaps:")

for gap in result["skill_gaps"]:
    print("✗", gap)


print("\n💡 Improvement Suggestions:")

for suggestion in result["suggestions"]:
    print("•", suggestion)


print("\n======================================")