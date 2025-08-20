import os

OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "gemma:2b"
CHROMA_DB_DIR = "./resume_chroma_db"
COLLECTION_NAME = "resume_collection"
CHUNK_SIZE = 800  # Smaller chunks for resumes
CHUNK_OVERLAP = 100

# Ensure ChromaDB directory exists
os.makedirs(CHROMA_DB_DIR, exist_ok=True)

# Resume-specific prompt templates
RESUME_PROMPTS = {
    "general": """You are an expert resume analyzer and technical recruiter. 
    Analyze the resume context below to provide comprehensive insights about the candidate.

    Context: {context}
    Question: {question}

    Provide structured, professional analysis focusing on qualifications, experience, and role fit.
    Answer: """,
    "technical": """You are a senior technical recruiter. Focus on technical skills analysis.
    
    Extract and analyze:
    - Programming languages and proficiency
    - Frameworks, tools, and technologies
    - Years of experience with each skill
    - Technical certifications
    - Project complexity indicators

    Context: {context}
    Question: {question}

    Structure as: 1) Primary Skills 2) Secondary Skills 3) Tools/Frameworks 4) Experience Level
    Answer: """,
    "experience": """You are an HR professional analyzing work experience and career progression.
    
    Focus on:
    - Career timeline and progression
    - Job responsibilities and scope
    - Achievements and impact
    - Leadership and management experience
    - Industry background

    Context: {context}
    Question: {question}

    Structure as: 1) Career Summary 2) Key Positions 3) Achievements 4) Progression Analysis
    Answer: """,
    "match": """You are evaluating candidate-role fit. Analyze how well this candidate matches specific requirements.
    
    Assess:
    - Required skills alignment
    - Experience level match
    - Industry background relevance
    - Growth potential
    - Potential concerns

    Context: {context}
    Question: {question}

    Structure as: 1) Match Score 2) Strengths 3) Gaps 4) Recommendations
    Answer: """,
}

# Quick analysis questions
QUICK_QUESTIONS = {
    "Summary": "Provide a comprehensive professional summary of this candidate including their key strengths, experience level, and notable achievements.",
    "Technical Skills": "List all technical skills mentioned, categorized by proficiency level and years of experience.",
    "Experience": "Summarize the candidate's work experience including roles, companies, duration, and key responsibilities.",
    "Education": "Detail the candidate's educational background, certifications, and relevant training.",
    "Achievements": "Highlight the candidate's most significant professional achievements and accomplishments.",
    "Leadership": "Identify any leadership, management, or team collaboration experience.",
    "Career Progression": "Analyze the candidate's career progression and growth trajectory.",
    "Red Flags": "Identify any potential concerns such as employment gaps, frequent job changes, or skill misalignments.",
}
