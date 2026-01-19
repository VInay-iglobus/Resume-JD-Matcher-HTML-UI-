#!/usr/bin/env python
"""Test education extraction and matching"""

from matching_engine import check_education_match, normalize_education

print("=" * 70)
print("EDUCATION MATCHING TESTS")
print("=" * 70)

# Test 1: Bachelor vs Bachelor
print("\n✓ Test 1: Bachelor vs Bachelor")
resume1 = {'education': [{'degree': 'Bachelor of Science in Computer Science'}]}
jd1 = {'requiredEducation': 'Bachelor Degree'}
result1 = check_education_match(resume1, jd1)
print(f"  Resume: {resume1['education'][0]['degree']}")
print(f"  Required: {jd1['requiredEducation']}")
print(f"  Met: {result1['met']}, Score: {result1['score']}/25, {result1['percentage']}%")
print(f"  Details: {result1['details']}")

# Test 2: Master vs Bachelor (overqualified)
print("\n✓ Test 2: Master vs Bachelor (OVERQUALIFIED)")
resume2 = {'education': [{'degree': 'Master of Technology (M.Tech) in Computer Science'}]}
jd2 = {'requiredEducation': 'Bachelor Degree'}
result2 = check_education_match(resume2, jd2)
print(f"  Resume: {resume2['education'][0]['degree']}")
print(f"  Required: {jd2['requiredEducation']}")
print(f"  Met: {result2['met']}, Score: {result2['score']}/25, {result2['percentage']}%")
print(f"  Details: {result2['details']}")

# Test 3: Diploma vs Bachelor (underqualified)
print("\n✓ Test 3: Diploma vs Bachelor (UNDERQUALIFIED)")
resume3 = {'education': [{'degree': 'Diploma in IT'}]}
jd3 = {'requiredEducation': 'Bachelor Degree'}
result3 = check_education_match(resume3, jd3)
print(f"  Resume: {resume3['education'][0]['degree']}")
print(f"  Required: {jd3['requiredEducation']}")
print(f"  Met: {result3['met']}, Score: {result3['score']}/25, {result3['percentage']}%")
print(f"  Details: {result3['details']}")

# Test 4: No education specified in resume
print("\n✓ Test 4: Empty Education vs Bachelor Required")
resume4 = {'education': []}
jd4 = {'requiredEducation': 'Bachelor Degree'}
result4 = check_education_match(resume4, jd4)
print(f"  Resume: [No education]")
print(f"  Required: {jd4['requiredEducation']}")
print(f"  Met: {result4['met']}, Score: {result4['score']}/25, {result4['percentage']}%")
print(f"  Details: {result4['details']}")

# Test 5: No requirement specified
print("\n✓ Test 5: Bachelor vs No Requirement")
resume5 = {'education': [{'degree': 'Bachelor of Commerce'}]}
jd5 = {'requiredEducation': 'Not specified'}
result5 = check_education_match(resume5, jd5)
print(f"  Resume: {resume5['education'][0]['degree']}")
print(f"  Required: {jd5['requiredEducation']}")
print(f"  Met: {result5['met']}, Score: {result5['score']}/25, {result5['percentage']}%")
print(f"  Details: {result5['details']}")

# Test 6: PhD vs Master
print("\n✓ Test 6: PhD vs Master (OVERQUALIFIED)")
resume6 = {'education': [{'degree': 'PhD in Computer Science'}]}
jd6 = {'requiredEducation': 'Master'}
result6 = check_education_match(resume6, jd6)
print(f"  Resume: {resume6['education'][0]['degree']}")
print(f"  Required: {jd6['requiredEducation']}")
print(f"  Met: {result6['met']}, Score: {result6['score']}/25, {result6['percentage']}%")
print(f"  Details: {result6['details']}")

# Test 7: B.Tech vs Bachelor (variant)
print("\n✓ Test 7: B.Tech vs Bachelor (VARIANT)")
resume7 = {'education': [{'degree': 'B.Tech in Electronics'}]}
jd7 = {'requiredEducation': 'Bachelor Degree'}
result7 = check_education_match(resume7, jd7)
print(f"  Resume: {resume7['education'][0]['degree']}")
print(f"  Required: {jd7['requiredEducation']}")
print(f"  Met: {result7['met']}, Score: {result7['score']}/25, {result7['percentage']}%")
print(f"  Details: {result7['details']}")

# Test 8: MBA vs Master
print("\n✓ Test 8: MBA vs Master (VARIANT)")
resume8 = {'education': [{'degree': 'Master of Business Administration (MBA)'}]}
jd8 = {'requiredEducation': 'Master'}
result8 = check_education_match(resume8, jd8)
print(f"  Resume: {resume8['education'][0]['degree']}")
print(f"  Required: {jd8['requiredEducation']}")
print(f"  Met: {result8['met']}, Score: {result8['score']}/25, {result8['percentage']}%")
print(f"  Details: {result8['details']}")

# Test 9: Normalize education test
print("\n" + "=" * 70)
print("EDUCATION NORMALIZATION TESTS")
print("=" * 70)
test_degrees = [
    "Bachelor of Science in Computer Science",
    "B.Tech in Electronics",
    "Master of Technology",
    "MBA",
    "PhD",
    "Diploma",
    "High School",
    "B.S. in Mathematics",
    "M.Tech",
    "Doctorate in Philosophy"
]

for degree in test_degrees:
    normalized, level = normalize_education(degree)
    level_name = {0: "High School", 1: "Diploma", 2: "Bachelor", 3: "Master", 4: "PhD"}
    print(f"  {degree:40s} → {normalized:20s} (Level {level}: {level_name.get(level, 'Unknown')})")

print("\n" + "=" * 70)
print("✅ ALL TESTS COMPLETED")
print("=" * 70)
