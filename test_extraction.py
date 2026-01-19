"""
Test script to debug extraction issues
Run this to see exactly what's being extracted
"""

import sys
sys.path.insert(0, '/path/to/your/project')

from llm_extraction import extract_structured_data_stable
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ==================== TEST RESUME ====================
TEST_RESUME = """
John Doe
Senior Software Engineer
john@example.com | LinkedIn: linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Experienced Software Engineer with 8+ years of expertise in full-stack development, 
cloud architecture, and team leadership. Proven track record delivering scalable 
applications using Python, JavaScript, and modern cloud technologies.

EXPERIENCE

Senior Software Engineer | TechCorp Inc | 2020 - Present
- Led development team of 5 engineers building microservices using Python and Node.js
- Designed and implemented real-time data processing pipeline handling 1M+ events/day
- Mentored junior developers and conducted code reviews
- Technologies: Python, JavaScript, React, Node.js, Docker, Kubernetes, AWS

Software Engineer | DataSystems LLC | 2018 - 2020
- Developed full-stack web applications using JavaScript, React, and Express.js
- Built REST APIs serving 10K+ daily active users
- Implemented automated testing and CI/CD pipelines with Jenkins
- Technologies: JavaScript, React, Node.js, MongoDB, PostgreSQL, AWS

Junior Developer | StartupXYZ | 2016 - 2018
- Built responsive web interfaces using HTML, CSS, and JavaScript
- Wrote backend services in Python using Django framework
- Collaborated with product team on feature requirements
- Technologies: Python, Django, JavaScript, jQuery, MySQL

EDUCATION
B.Tech in Computer Science
Indian Institute of Technology (IIT), New Delhi
Graduated: 2016 GPA: 3.8/4.0

TECHNICAL SKILLS
- Languages: Python, JavaScript, TypeScript, SQL, Bash
- Frontend: React, HTML, CSS, Redux, Angular
- Backend: Node.js, Django, Flask, Express.js
- Databases: PostgreSQL, MongoDB, MySQL, Redis
- DevOps: Docker, Kubernetes, AWS, Jenkins, Git
- Soft Skills: Team Leadership, Project Management, Mentoring, Communication

CERTIFICATIONS
- AWS Certified Solutions Architect (2021)
- Kubernetes Administrator Certification (2022)
- Google Cloud Associate Cloud Engineer (2020)

PROJECTS
- Built real-time chat application: React + Node.js + WebSocket
- Developed ML data pipeline: Python + Spark + Kubernetes
- Created mobile app backend: Python + GraphQL + PostgreSQL
"""

# ==================== TEST JD ====================
TEST_JD = """
Senior Full-Stack Engineer
TechCorp Inc - San Francisco, CA (Remote Available)

Job Description
We are seeking an experienced Senior Full-Stack Engineer to join our growing team. 
You will be responsible for designing and implementing scalable web applications, 
mentoring junior developers, and collaborating with product teams.

Requirements
- 5+ years of professional software development experience
- Strong proficiency in JavaScript and Python
- Experience with React, Node.js, and modern web frameworks
- Working knowledge of SQL and NoSQL databases
- Experience with Docker and Kubernetes
- Bachelor's Degree in Computer Science or related field
- Excellent communication and problem-solving skills

Key Responsibilities
- Design and develop scalable full-stack web applications
- Architect microservices-based systems
- Conduct code reviews and mentor junior developers
- Collaborate with product and design teams
- Implement automated testing and CI/CD pipelines
- Optimize application performance and security

Technical Skills Required
JavaScript, Python, React, Node.js, Express.js, HTML, CSS, PostgreSQL, MongoDB, 
Docker, Kubernetes, AWS, REST APIs, GraphQL, Git, Jenkins, Agile, SQL

Preferred Skills
TypeScript, Vue.js, Microservices Architecture, Machine Learning, Apache Spark, 
Terraform, AWS Lambda, RabbitMQ

Benefits
- Competitive salary: $150,000 - $200,000
- Health insurance and 401(k) matching
- Remote work flexibility
- Professional development budget
- Flexible hours and work-life balance

Location: San Francisco, CA (Remote)
Employment Type: Full-time
"""

# ==================== RUN TEST ====================

def test_extraction():
    print("\n" + "="*70)
    print("🧪 TESTING EXTRACTION")
    print("="*70 + "\n")
    
    # Test resume
    print("📄 EXTRACTING RESUME...")
    try:
        resume_data = extract_structured_data_stable(TEST_RESUME, "Resume")
        print("\n✅ RESUME EXTRACTION SUCCESS\n")
        print(json.dumps(resume_data, indent=2))
    except Exception as e:
        print(f"\n❌ RESUME EXTRACTION FAILED: {e}\n")
    
    # Test JD
    print("\n\n📋 EXTRACTING JOB DESCRIPTION...")
    try:
        jd_data = extract_structured_data_stable(TEST_JD, "Job Description")
        print("\n✅ JD EXTRACTION SUCCESS\n")
        print(json.dumps(jd_data, indent=2))
    except Exception as e:
        print(f"\n❌ JD EXTRACTION FAILED: {e}\n")

if __name__ == "__main__":
    test_extraction()