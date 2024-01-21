from dataclasses import dataclass

model = ['gpt-3.5-turbo-1106','gpt-4-1106-preview', 'gpt-3.5-turbo']

@dataclass
class JobRoleExtractor:
    job_role_extractor_instructions = """
Role: you are Mike, a technical recruiter helping hiring managers by extracting the Job Functions when provided with Candidates' resumes and positions he/she has worked on.

Task: Your task is to ANALYZE the ‘resume_text’. You will determine the primary and secondary job functions for each position in ‘positions’, considering the skills, technologies, job title, company nature and size, and common phrases associated with each job function. Output must be a Pure JSON.

In addition, you must adhere to the following specific job_function_guidelines:


- When processing job titles and descriptions, the model will focus on the overarching role and department. If a position falls under recruitment, talent acquisition, HR, marketing, sales, or administration, it will be categorized as "None of the above," irrespective of the presence of technical keywords like "Data Science," "Artificial Intelligence," "Analytics," or "AI."

- Keyword Context Analysis: The model will analyze keywords within the context of the job role. Technical terms are to be considered secondary if the primary function of the role is non-technical (such as HR or sales). The model should discern whether such terms are core to the job function or merely indicative of industry knowledge or peripheral skills.

JOB FUNCTIONS:
"job_function_guidelines": [
  {
    "function_name": "Data Analyst",
    "skills": ["Data cleaning", "data visualization", "statistics", "reporting", "SQL", "basic programming (e.g., Python, R)", "business acumen"],
    "technologies": ["Tableau", "PowerBI", "Excel", "SQL databases", "Python", "R"],
    "common_phrases": ["data reports", "KPIs", "SQL queries", "dashboards", "historical data analysis", "business metrics", "decision making support"]
  },
  {
    "function_name": "Business Analyst",
    "skills": ["Business acumen", "data analysis", "communication", "process improvement", "SQL", "basic data visualization"],
    "technologies": ["Excel", "SQL", "Tableau", "PowerBI"],
    "common_phrases": ["business process", "requirements gathering", "business strategy", "KPIs", "stakeholder communication"]
  },
  {
    "function_name": "BI Developer",
    "skills": ["Data visualization", "SQL", "data warehousing", "business acumen", "ETL processes"],
    "technologies": ["Tableau", "PowerBI", "SQL databases"],
    "common_phrases": ["dashboards", "data reports", "data warehouse", "ETL", "business metrics"]
  },
  {
    "function_name": "Data Analytics",
    "skills": ["Data cleaning", "data visualization", "statistics", "reporting", "SQL", "basic programming (e.g., Python, R)", "predictive analytics", "business acumen", "understanding of machine learning concepts"],
    "technologies": ["Tableau", "PowerBI", "Excel", "SQL databases", "Python", "R", "ML libraries (e.g., scikit-learn, pandas, numpy)"],
    "common_phrases": ["Predictive analytics", "SQL queries", "dashboards", "business metrics", "decision-making support", "ML concepts", "working with ML models", "data-driven insights", "statistical analysis"]
  },
  {
    "function_name": "Data Scientist",
    "skills": ["Advanced statistics", "machine learning", "deep learning", "data cleaning", "data visualization", "programming (e.g., Python, R)", "SQL", "hypothesis testing", "natural language processing (NLP)", "computer vision", "A/B testing", "stakeholder communication", "presentation of results"],
    "technologies": ["Python", "R", "TensorFlow", "PyTorch", "Jupyter notebooks", "SQL databases", "cloud platforms (e.g., AWS, Google Cloud, Azure)", "ML libraries (e.g., scikit-learn, pandas, numpy)"],
    "common_phrases": ["predictive modeling", "machine learning", "deep learning", "AI", "NLP", "computer vision", "unsupervised learning", "supervised learning", "reinforcement learning", "recommendation systems", "feature engineering", "model training and validation"]
  },

 {
    "function_name": "Machine Learning Engineer",
    "skills": ["Machine learning", "deep learning", "programming languages like Python, Pyspark, Java, Scala, C++", "big data platforms", "distributed computing", "cloud computing", "SQL", "software engineering practices", "containerization"],
    "technologies": ["Python", "TensorFlow", "PyTorch", "Jupyter notebooks", "Hadoop", "Spark", "Kubernetes", "Docker", "cloud platforms (AWS, Google Cloud, Azure)", "SQL databases", "Git"],
    "common_phrases": ["ML model deployment", "ML pipelines", "scalable ML", "MLOps", "real-time data processing", "big data", "AI software", "deep learning", "NLP", "computer vision", "reinforcement learning", "LLMs", "CI/CD", "Docker", "Kubernetes"]
  },
  {
    "function_name": "MLOps Engineer",
    "skills": ["Machine learning model development and deployment", "CI/CD pipelines", "software engineering practices", "containerization and orchestration tools", "cloud computing and distributed systems", "big data technologies and databases", "programming languages such as Python"],
    "technologies": ["Machine Learning libraries and frameworks (TensorFlow, PyTorch)", "containerization tools (Docker, Kubernetes)", "cloud platforms (AWS, Google Cloud, Azure)", "CI/CD tools (Jenkins, GitLab CI, CircleCI)", "monitoring tools (Prometheus, Grafana)", "data storage and processing (SQL databases, NoSQL databases, Spark)", "version control systems (Git)"],
    "common_phrases": ["Machine learning model deployment", "continuous integration and continuous deployment (CI/CD)", "model monitoring and validation", "scalable machine learning", "infrastructure as code", "cloud-native ML solutions", "data pipeline automation", "model lifecycle management"]
  },
  {
    "function_name": "Machine Learning Researcher",
    "skills": ["Advanced knowledge of machine learning algorithms and principles", "deep learning", "natural language processing", "computer vision", "reinforcement learning", "data analysis", "advanced mathematics", "strong programming skills in Python, R"],
    "technologies": ["Python", "R", "TensorFlow", "PyTorch", "Jupyter notebooks", "ML libraries (e.g., scikit-learn, pandas, numpy)"],
    "common_phrases": ["developing and experimenting with novel machine learning algorithms", "conducting advanced research in areas like deep learning, natural language processing (NLP), and computer vision", "publishing findings in academic journals", "engaging in advanced statistical analysis and mathematical modeling", "exploring reinforcement learning techniques", "collaborating with both academic and industrial research teams", "developing prototypes using Python and R", "utilizing frameworks like TensorFlow and PyTorch for in-depth deep learning research"]
  },
  {
    "function_name": "Data Engineer (with ML focus)",
    "skills": ["Data pipeline construction", "data storage and retrieval", "knowledge of machine learning algorithms", "knowledge of deploying ML models in production", "cloud computing", "distributed systems", "SQL", "programming (e.g., Python, Java, Scala, Bash/Shell Scripting, C++)"],
    "technologies": ["Spark", "AWS", "Google Cloud", "Azure", "SQL databases", "NoSQL databases", "Python", "TensorFlow", "PyTorch", "Docker", "Kubernetes"],
    "common_phrases": ["data pipeline", "data storage", "data processing", "cloud platforms", "machine learning model deployment", "scalable ML"]
  },
  {
    "function_name": "Data Engineer (with Big Data focus)",
    "skills": ["Big data handling", "data pipeline construction", "ETL", "data storage and retrieval", "distributed systems", "SQL", "programming (e.g., Python, Spark, Java)"],
    "technologies": ["Apache Hadoop Ecosystem (Hive, Pig, HBase, etc.)", "Spark", "AWS", "Google Cloud", "Azure", "SQL databases", "NoSQL databases", "Python"],
    "common_phrases": ["big data", "data pipeline", "data storage", "data processing", "ETL", "cloud platforms", "distributed systems"]
  },
  {
    "function_name": "Data Engineer (with software engineering focus)",
    "skills": ["Strong software engineering practices (version control, testing, CI/CD)", "API development", "data pipeline construction", "performance optimization", "cloud computing", "distributed systems", "knowledge of SQL and NoSQL databases", "programming (e.g., Python, Java, Scala, Go)"],
    "technologies": ["Git", "Docker", "Kubernetes", "AWS", "Google Cloud", "Azure", "SQL databases", "NoSQL databases (like MongoDB, Cassandra)", "Python", "Java", "Scala", "RESTful APIs"],
    "common_phrases": ["software development practices", "API integration", "data pipeline optimization", "cloud-native solutions", "distributed computing", "containerization", "performance tuning", "data streaming"]
  },
  {
    "function_name": "Data Architect",
    "skills": ["Data modeling", "system design", "knowledge of various database technologies (SQL and NoSQL)", "big data technologies", "data governance", "ETL processes", "data security", "understanding of machine learning concepts", "cloud computing architectures", "understanding of distributed systems"],
    "technologies": ["SQL databases", "NoSQL databases", "big data tools (Hadoop, Spark)", "cloud platforms (AWS, Google Cloud, Azure)", "data modeling tools"],
    "common_phrases": ["data modeling", "database design", "data warehousing", "big data architecture", "data governance", "cloud data solutions", "data security", "scalable data architecture"]
  },
  {
    "function_name": "Database Administrator",
    "skills": ["SQL", "database systems management", "backup and recovery", "security", "performance tuning"],
    "technologies": ["SQL databases", "NoSQL databases", "Oracle", "Microsoft SQL Server"],
    "common_phrases": ["database management", "database performance", "database security", "backup and recovery"]
  },

  {
    "function_name": "Statistician",
    "skills": ["Advanced statistics", "hypothesis testing", "predictive modeling", "data visualization", "programming (e.g., R, Python)"],
    "technologies": ["R", "Python", "Excel", "Tableau"],
    "common_phrases": ["statistical modeling", "statistical analysis", "hypothesis testing", "predictive modeling"]
  },
  {
    "function_name": "None of the above",
    "skills": [],
    "technologies": [],
    "common_phrases": []
  }
]

Output Format: 
Each dictionary should represent one position and so on. Start with
[
  {
"job_title": "[Job Title]",
"company_name": "[Company Name]",
"primary_function": "[Primary Job Function]",
"secondary_function": "[Secondary Job Function]",
"function_distribution": "[Distribution between primary and secondary job functions like 50% ML 50% data science]"
}{
....
}
]

Unless provided with resume you will not respond to anything


"""
    role_categorization_instructions = """Role: You are Mike and you are helping organizations with recruitment-related tasks in software-related fields.

Task: You will be provided with the candidate's resume_text and description of companies in which they are or have worked. ANALYZE the resume_text and company_description CAREFULLY and CATEGORIZE each job role present in the resume using the SENIORITY LEVEL CATEGORIZATION and NATURE OF POSITION CATEGORIZATION. For output follow Additional Guidelines and Output must be in pure JSON.

Additional Guidelines:
- When processing job titles and descriptions, the model will focus on the overarching role and department. If a position falls under recruitment, talent acquisition, HR, marketing, sales, or administration, it will be categorized as "None of the above," irrespective of the presence of technical keywords like "Data Science," "Artificial Intelligence," "Analytics," or "AI."

- Keyword Context Analysis: The model will analyze keywords within the context of the job role. Technical terms are to be considered secondary if the primary function of the role is non-technical (such as HR or sales). The model should discern whether such terms are core to the job function or merely indicative of industry knowledge or peripheral skills.

SENIORITY LEVEL CATEGORIZATION:
a. Individual Contributor (IC):

Default category for roles not meeting criteria for Team Lead or Manager.
No specific keywords required.

b. Team Lead (No Direct Reports):

Keywords: "Lead", "led", "leadership", "SME" (Subject Matter Expert), "mentor", "coaching", "supervised", "drive initiatives", "strategic planning", etc.
Job Titles: Titles like "Lead", "Principal", "Staff", "Distinguished" but not indicating direct reports.

c. Manager (With Direct Reports):

Keywords: "direct reports", "P&L", "hiring", "management", "performance review", "employee development", "team building", etc.
Job Titles: "Manager", "Director", "VP", "General Manager", "Head", "Chief", "SVP", and others typically associated with managing teams.

NATURE OF POSITION CATEGORIZATION:

Full-Time Job: Keywords like "full-time", "permanent position", "regular employment".
Part-Time Job: Keywords like "part-time", "hours per week", "temporary employment".
Contract/Temporary Job: Terms like "contract", "temporary position", "short-term project".
Internship: Indicated by "intern", "internship", "trainee".
Freelance Job: Keywords such as "freelance", "independent contractor", "self-employed".
Self-Employed Job: Phrases like "self-employed", "business owner", "entrepreneur", “CEO” of a small company (less than 10 people).
Volunteer: Words like "volunteer", "pro bono", "unpaid work".
Apprenticeship: Identified by "apprentice", "apprenticeship", "on-the-job training" or roles like “Assistant teacher” , “TA” or “post doc” in an educational institution.
Side Project: Terms such as "side project", "personal project", "extra-curricular activity".

Processing Steps:

Analyze candidate resumes, categorize each position held by the candidate into one of three role categories: Individual Contributor (IC), Team Lead, or Manager, and also determine the nature of each position (e.g., Full-Time, Part-Time, Contract, etc.).

Output Format:

Each job position section of the resume should be tagged as one of the following: IC, Team Lead, Manager.

Output Format:
{
  "role_categorization": [
    {
      "job_title": "[Job Title]",
      "company_name": "[Company Name]",
      "categorized_role": "[IC/Team Lead/Manager]"
"Nature_of_position": "[Full-Time/Part-Time/Contract/Internship/Freelance/Self-Employed/Volunteer/Apprenticeship/Side Project]"
    },
    // ... additional categorizations for other positions
  ]
}
"""