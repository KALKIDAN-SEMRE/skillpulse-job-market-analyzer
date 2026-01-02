"""
Data extraction logic for job posts.
Extracts salary, skills, and job titles from raw text.
"""
import re
from typing import List, Optional, Set


# Predefined list of tech skills to look for in job posts
# This is a basic list for Day 1 - can be expanded later
TECH_SKILLS = [
    # Programming Languages
    'Python', 'JavaScript', 'Java', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
    'PHP', 'Ruby', 'Swift', 'Kotlin', 'Scala', 'R', 'Dart', 'Perl',
    
    # Web Frameworks
    'React', 'Vue', 'Angular', 'Django', 'Flask', 'FastAPI', 'Express',
    'Next.js', 'Nuxt', 'Svelte', 'Laravel', 'Spring', 'ASP.NET',
    
    # Backend/Database
    'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch', 'Cassandra',
    'SQLite', 'DynamoDB', 'Oracle', 'SQL Server',
    
    # Cloud & DevOps
    'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform', 'Ansible',
    'Jenkins', 'GitLab CI', 'GitHub Actions', 'Linux', 'Bash',
    
    # Frontend Tools
    'HTML', 'CSS', 'SASS', 'LESS', 'Webpack', 'Vite', 'npm', 'yarn',
    
    # Data Science & ML
    'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Pandas',
    'NumPy', 'Scikit-learn', 'Jupyter', 'Data Science',
    
    # Mobile
    'React Native', 'Flutter', 'iOS', 'Android', 'Xamarin',
    
    # Other Tools
    'Git', 'GitHub', 'GitLab', 'Jira', 'Agile', 'Scrum', 'REST API',
    'GraphQL', 'Microservices', 'Node.js', 'npm', 'yarn'
]


def extract_salary(text: str) -> Optional[str]:
    """
    Extract salary information from job post text using regex patterns.
    
    Looks for patterns like:
    - $50,000 - $80,000
    - $50k-$80k
    - 50000-80000
    - 50k-80k
    - $100k/year
    - etc.
    
    Args:
        text: Raw job post text
        
    Returns:
        Extracted salary string or None if not found
    """
    # Common salary patterns
    patterns = [
        # $50,000 - $80,000 or $50,000-$80,000
        r'\$?\s*(\d{1,3}(?:,\d{3})*(?:k)?)\s*[-–—]\s*\$?\s*(\d{1,3}(?:,\d{3})*(?:k)?)\s*(?:per\s+year|/year|annually|USD|EUR|RUB)?',
        # $100k/year or $100k per year
        r'\$?\s*(\d{1,3}(?:,\d{3})*(?:k)?)\s*(?:per\s+year|/year|annually|USD|EUR|RUB)',
        # Range with k suffix: 50k-80k
        r'(\d{1,3}k)\s*[-–—]\s*(\d{1,3}k)',
        # Single salary: $100k
        r'\$?\s*(\d{1,3}(?:,\d{3})*(?:k)?)\s*(?:USD|EUR|RUB)',
    ]
    
    text_upper = text.upper()
    
    for pattern in patterns:
        match = re.search(pattern, text_upper, re.IGNORECASE)
        if match:
            # Clean up and return the matched salary
            salary_text = match.group(0).strip()
            return salary_text
    
    return None


def extract_skills(text: str) -> Set[str]:
    """
    Extract tech skills from job post text using keyword matching.
    
    Args:
        text: Raw job post text
        
    Returns:
        Set of skill names found in the text
    """
    found_skills = set()
    text_upper = text.upper()
    
    # Check each skill (case-insensitive)
    for skill in TECH_SKILLS:
        skill_upper = skill.upper()
        
        # Look for whole word matches to avoid false positives
        # Using word boundaries for better matching
        pattern = r'\b' + re.escape(skill_upper) + r'\b'
        if re.search(pattern, text_upper):
            found_skills.add(skill)  # Add original case
    
    return found_skills


def extract_job_title(text: str) -> Optional[str]:
    """
    Infer job title from job post text.
    This is a basic implementation for Day 1.
    
    Looks for common patterns like:
    - "Looking for a Senior Python Developer"
    - "Hiring: Backend Engineer"
    - "Position: Data Scientist"
    
    Args:
        text: Raw job post text
        
    Returns:
        Inferred job title or None
    """
    # Common job title patterns
    patterns = [
        r'(?:looking\s+for|hiring|seeking|vacancy|position|role):?\s+([A-Z][a-zA-Z\s]{10,50}?)(?:\s+with|\s+for|\.|$)',
        r'(?:we\s+need|need|required):?\s+([A-Z][a-zA-Z\s]{10,50}?)(?:\s+developer|\s+engineer|\s+specialist)',
    ]
    
    # First, try to find explicit title patterns
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            # Clean up common prefixes
            title = re.sub(r'^(a|an|the)\s+', '', title, flags=re.IGNORECASE)
            if len(title) > 5 and len(title) < 100:
                return title
    
    # Fallback: Look for common job titles in the first few lines
    lines = text.split('\n')[:5]
    common_titles = [
        'Developer', 'Engineer', 'Programmer', 'Architect', 'Designer',
        'Analyst', 'Scientist', 'Manager', 'Lead', 'Senior', 'Junior'
    ]
    
    for line in lines:
        line_clean = line.strip()
        if any(title_word in line_clean for title_word in common_titles):
            # Extract a reasonable chunk
            words = line_clean.split()[:5]
            if len(words) >= 2:
                potential_title = ' '.join(words)
                if len(potential_title) < 100:
                    return potential_title
    
    return None

