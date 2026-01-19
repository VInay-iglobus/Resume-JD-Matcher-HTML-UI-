from difflib import SequenceMatcher
import logging
import re
from skills_analogy import get_skill_group, SKILL_ANALOGY

logger = logging.getLogger(__name__)

# ==================== UTILITY ====================

def normalize_skill(skill):
    """Normalize skill for comparison"""
    if not skill:
        return ""
    skill = str(skill).lower().strip()
    skill = re.sub(r'[^a-z0-9\s]', '', skill)
    skill = ' '.join(skill.split())
    return skill

# ==================== SKILL MATCHING ====================

def find_skill_match(candidate_skill, required_skill, similarity_threshold=0.70):
    """Find skill match with multiple strategies including analogy mapping"""
    
    cand_norm = normalize_skill(candidate_skill)
    req_norm = normalize_skill(required_skill)
    
    if not cand_norm or not req_norm:
        return False, "invalid", 0
    
    # Strategy 1: Exact match
    if cand_norm == req_norm:
        return True, "exact", 1.0
    
    # Strategy 2: Check skill analogy mapping
    # If both skills belong to the same skill group, they're equivalent
    try:
        cand_group = get_skill_group(candidate_skill)
        req_group = get_skill_group(required_skill)
        
        if cand_group and req_group and cand_group == req_group:
            # Same skill family (e.g., React and ReactJS)
            return True, "analogy", 0.95
    except:
        pass
    
    # Strategy 3: Fuzzy match
    similarity = SequenceMatcher(None, cand_norm, req_norm).ratio()
    if similarity >= similarity_threshold:
        return True, "fuzzy", similarity
    
    # Strategy 4: Substring
    if len(req_norm) > 3 and len(cand_norm) > 3:
        if cand_norm in req_norm or req_norm in cand_norm:
            return True, "substring", 0.88
    
    return False, "no_match", 0

# ==================== EXPERIENCE ====================

def check_experience_match(resume_data, jd_data):
    """Check experience match"""
    try:
        candidate_years = float(resume_data.get('totalYearsExperience', 0) or 0)
        required_years = float(jd_data.get('minExperienceYears', 0) or 0)
    except:
        candidate_years = 0
        required_years = 0
    
    met = candidate_years >= required_years
    
    if required_years == 0:
        score = 35
        percentage = 100
        details = f"No specific experience required. Candidate has {int(candidate_years)} years. ✅ MATCHES."
    elif candidate_years >= required_years:
        score = 35
        percentage = 100
        details = f"Candidate has {int(candidate_years)} years, Required: {int(required_years)} years. ✅ MATCHES."
    else:
        percentage = int((candidate_years / required_years) * 100) if required_years > 0 else 0
        score = int((candidate_years / required_years) * 35) if required_years > 0 else 0
        score = max(1, score)
        details = f"Candidate has {int(candidate_years)} years, Required: {int(required_years)} years. ⚠️ {percentage}% match."
    
    return {
        "met": met,
        "candidateExperience": int(candidate_years),
        "requiredExperience": int(required_years),
        "details": details,
        "score": score,
        "percentage": min(100, percentage)
    }

# ==================== EDUCATION ====================

EDUCATION_HIERARCHY = {
    "phd": 4,
    "doctorate": 4,
    "master": 3,
    "m.tech": 3,
    "mba": 3,
    "bachelor": 2,
    "b.tech": 2,
    "b.s": 2,
    "b.a": 2,
    "diploma": 1,
    "high school": 0
}

def normalize_education(degree):
    """Normalize education degree"""
    if not degree:
        return "not specified", 0
    
    degree_lower = str(degree).lower().strip()
    
    for key, value in EDUCATION_HIERARCHY.items():
        if key in degree_lower:
            return key, value
    
    return degree_lower, 0

def check_education_match(resume_data, jd_data):
    """Check education match - considers highest degree"""
    candidate_degree = "not specified"
    candidate_level = 0
    
    education_list = resume_data.get('education', [])
    
    # Find the HIGHEST degree from all education entries
    if education_list and isinstance(education_list, list) and len(education_list) > 0:
        # Get the highest education level
        highest_level = 0
        highest_degree = "not specified"
        
        for edu_item in education_list:
            if isinstance(edu_item, dict):
                degree_str = edu_item.get('degree', 'not specified')
            else:
                degree_str = str(edu_item) if edu_item else 'not specified'
            
            degree_norm, level = normalize_education(degree_str)
            
            if level > highest_level:
                highest_level = level
                highest_degree = degree_str
        
        candidate_degree = highest_degree if highest_degree != "not specified" else "not specified"
        candidate_level = highest_level
    
    required_degree = jd_data.get('requiredEducation', 'not specified')
    required_degree_norm, required_level = normalize_education(required_degree)
    
    met = candidate_level >= required_level
    
    if required_level == 0 or required_degree == "not specified":
        score = 25
        percentage = 100
        details = f"No specific education required. ✅ MATCHES."
    elif candidate_level >= required_level:
        score = 25
        percentage = 100
        if candidate_level > required_level:
            details = f"Candidate is OVERQUALIFIED! Has {candidate_degree} (required: {required_degree}). 🎓 EXCELLENT!"
        else:
            details = f"Candidate has {candidate_degree}, Required: {required_degree}. ✅ MATCHES."
    else:
        percentage = int((candidate_level / required_level) * 100) if required_level > 0 else 0
        score = int((candidate_level / required_level) * 25) if required_level > 0 else 0
        score = max(1, score)
        details = f"Candidate has {candidate_degree}, Required: {required_degree}. ⚠️ {percentage}% match."
    
    return {
        "met": met,
        "candidateDegree": candidate_degree,
        "requiredDegree": required_degree,
        "details": details,
        "score": score,
        "percentage": min(100, percentage),
        "isOverqualified": candidate_level > required_level and required_level > 0
    }

# ==================== SKILLS ====================

def check_skills_match(resume_data, jd_data):
    """Check skills match - STRICT"""
    
    # Extract candidate skills
    candidate_skills_list = resume_data.get('skills', [])
    candidate_skills = []
    
    for skill in candidate_skills_list:
        if isinstance(skill, dict):
            skill_name = skill.get('name', '').strip()
        else:
            skill_name = str(skill).strip() if skill else ''
        
        if skill_name:
            candidate_skills.append(skill_name)
    
    # Extract required skills
    required_skills_list = jd_data.get('requiredSkills', [])
    required_skills = [str(s).strip() for s in required_skills_list if s and str(s).strip()]
    
    if not required_skills:
        return {
            "met": True,
            "candidateSkillsCount": len(candidate_skills),
            "requiredSkillsCount": 0,
            "percentage": 100,
            "matchedSkills": candidate_skills,
            "missingSkills": [],
            "skillMatchDetails": [],
            "details": f"No specific skills required. Candidate has {len(candidate_skills)} skills. ✅ MATCHES.",
            "score": 40,
            "allCandidateSkills": candidate_skills
        }
    
    matched_skills = []
    missing_skills = []
    skill_match_details = []
    
    for req_skill in required_skills:
        skill_found = False
        best_match = None
        best_match_type = None
        best_confidence = 0
        
        for cand_skill in candidate_skills:
            is_match, match_type, confidence = find_skill_match(cand_skill, req_skill)
            
            if is_match:
                skill_found = True
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = cand_skill
                    best_match_type = match_type
        
        if skill_found:
            matched_skills.append(req_skill)
            skill_match_details.append({
                "required": req_skill,
                "matched": best_match,
                "type": best_match_type,
                "confidence": round(best_confidence, 2)
            })
        else:
            missing_skills.append(req_skill)
    
    percentage = int((len(matched_skills) / len(required_skills)) * 100) if required_skills else 0
    score = int((len(matched_skills) / len(required_skills)) * 40) if required_skills else 0
    score = max(1, score) if matched_skills else 0
    
    met = percentage >= 50
    
    if percentage == 0:
        details = f"❌ No matching skills! Candidate has {len(candidate_skills)}, Required: {len(required_skills)}"
    elif percentage < 25:
        details = f"⚠️ {len(matched_skills)}/{len(required_skills)} required skills ({percentage}%). Limited match."
    elif percentage < 50:
        details = f"⚠️ {len(matched_skills)}/{len(required_skills)} required skills ({percentage}%). Partial match."
    elif percentage < 75:
        details = f"✅ {len(matched_skills)}/{len(required_skills)} required skills ({percentage}%). Good match!"
    else:
        details = f"✅ {len(matched_skills)}/{len(required_skills)} required skills ({percentage}%). Excellent match!"
    
    return {
        "met": met,
        "candidateSkillsCount": len(matched_skills),
        "requiredSkillsCount": len(required_skills),
        "percentage": percentage,
        "matchedSkills": matched_skills,
        "missingSkills": missing_skills,
        "skillMatchDetails": skill_match_details,
        "details": details,
        "score": score,
        "allCandidateSkills": candidate_skills
    }

# ==================== MAIN ====================

ASSESSMENT_MAP = {
    90: {"text": "🌟 Excellent Match", "color": "green"},
    75: {"text": "✅ Great Match", "color": "green"},
    60: {"text": "👍 Good Match", "color": "blue"},
    40: {"text": "⚠️ Moderate Match", "color": "orange"},
    0: {"text": "❌ Poor Match", "color": "red"}
}

def get_assessment(score):
    """Get assessment based on score"""
    for threshold in sorted(ASSESSMENT_MAP.keys(), reverse=True):
        if score >= threshold:
            return ASSESSMENT_MAP[threshold]
    return ASSESSMENT_MAP[0]

def calculate_match(resume_data, jd_data):
    """Calculate overall match"""
    logger.info("\n" + "="*70)
    logger.info("🎯 MATCH CALCULATION STARTED")
    logger.info("="*70)
    
    try:
        # Check for empty data
        if not resume_data or not jd_data:
            raise Exception("Missing resume or JD data")
        
        experience_result = check_experience_match(resume_data, jd_data)
        education_result = check_education_match(resume_data, jd_data)
        skills_result = check_skills_match(resume_data, jd_data)
        
        criteria_analysis = {
            "experienceMatch": {
                "met": experience_result["met"],
                "candidateExperience": experience_result["candidateExperience"],
                "requiredExperience": experience_result["requiredExperience"],
                "details": experience_result["details"],
                "percentage": experience_result.get("percentage", 0)
            },
            "educationMatch": {
                "met": education_result["met"],
                "candidateDegree": education_result["candidateDegree"],
                "requiredDegree": education_result["requiredDegree"],
                "details": education_result["details"],
                "percentage": education_result.get("percentage", 0),
                "isOverqualified": education_result.get("isOverqualified", False)
            },
            "skillsMatch": {
                "met": skills_result["met"],
                "candidateSkillsCount": skills_result["candidateSkillsCount"],
                "requiredSkillsCount": skills_result["requiredSkillsCount"],
                "percentage": skills_result["percentage"],
                "matchedSkills": skills_result["matchedSkills"],
                "missingSkills": skills_result["missingSkills"],
                "skillMatchDetails": skills_result.get("skillMatchDetails", []),
                "allCandidateSkills": skills_result.get("allCandidateSkills", []),
                "details": skills_result["details"]
            }
        }
        
        section_scores = {
            "experienceMatch": experience_result["score"],
            "educationMatch": education_result["score"],
            "skillsMatch": skills_result["score"]
        }
        
        overall_score = sum(section_scores.values())
        overall_score = min(100, max(0, overall_score))
        
        assessment = get_assessment(overall_score)
        
        matched_count = sum(1 for v in criteria_analysis.values() if v.get('met'))
        total_criteria = 3
        
        summary = f"Matches {matched_count}/3 criteria. "
        if overall_score >= 75:
            summary += "Strong candidate for interview."
        elif overall_score >= 60:
            summary += "Good candidate to consider."
        elif overall_score >= 40:
            summary += "Moderate candidate with gaps."
        else:
            summary += "Significant improvement needed."
        
        recommendations = [
            experience_result['details'],
            education_result['details'],
            skills_result['details']
        ]
        
        gaps = []
        if not experience_result["met"]:
            gaps.append(f"Experience: {experience_result['percentage']}% match")
        if not education_result["met"]:
            gaps.append(f"Education: {education_result['percentage']}% match")
        if not skills_result["met"]:
            gaps.append(f"Skills: {skills_result['percentage']}% match")
        
        logger.info(f"\n📊 RESULTS:")
        logger.info(f"   Overall: {overall_score}/100 - {assessment['text']}")
        logger.info(f"   Experience: {section_scores['experienceMatch']}/35")
        logger.info(f"   Education: {section_scores['educationMatch']}/25")
        logger.info(f"   Skills: {section_scores['skillsMatch']}/40")
        logger.info("="*70 + "\n")
        
        return {
            "criteriaAnalysis": criteria_analysis,
            "sectionScores": section_scores,
            "overallScore": overall_score,
            "assessment": assessment,
            "gaps": gaps,
            "recommendations": recommendations,
            "summary": summary
        }
    
    except Exception as e:
        logger.error(f"❌ Match calculation error: {e}", exc_info=True)
        raise
