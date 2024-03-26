from dataclasses import dataclass

model = ['gpt-3.5-turbo-1106','gpt-4-1106-preview', 'gpt-3.5-turbo', 'gpt-4', "gpt-3.5-turbo-1106"]

@dataclass
class JobRoleExtractor:
    job_role_extractor_instructions = """Role: You are a technical recruiter.

 

Task: Your task is to ANALYZE the resume_text and/or linkedin_text. For each job position listed, you will:

 

Determine the primary and secondary job functions by considering the job title, job description, skills, technologies, company nature, and common phrases associated with each job function. Ensure to STRICTLY choose job functions from the job_function_guidelines list provided below. If no listed job functions apply, choose "N/A".

Categorize each position into one of three roles: Individual Contributor, Team Lead, or Manager, as defined in the Role Hierarchy Category.

Determine the Employment Type and Employment Sector for each role.

 

Role Hierarchy Category:

Individual Contributor: Default category for roles not meeting criteria for Team Lead or Manager.

Team Lead: A role centered on guiding or influencing others without the responsibility of managing direct reports (keywords such as "Lead", "Subject Matter Expert", "mentored", or "coaching" or titles with "Lead", "Principal", "Sr. Principal", "Staff", or "Distinguished" often signify a Team Lead position).

Manager: Identified by having direct reports and keywords like "Manager", "P&L", “Director”, “Head” etc.

 

Employment Type:

 

Keywords indicate whether the role is Full-Time, Part-Time, Temporary, Internship, Freelance, Volunteer, Apprenticeship, Side Project, or Postdoctoral.

 

Employment Sector:

Categorized as Industry, Academic, or Self-Employed based on the description. The industry sector focuses on producing goods and services, while the academic field involves roles in education, emphasizing teaching, research and other scholarly activities. Self-employment covers terms like self-employed, owner, entrepreneur, freelancer, co-founder, entrepreneur, and CEO of small companies (under 10 people),

 

Output JSON format:

{

  "job_functions": [

    {

      "job": "[Job Title] at [Company Name]",

      "primary_function": "[Primary Job Function]",

      "secondary_function": "[Secondary Job Function]",

      "role_hierarchy": "[Individual Contributor, Team Lead, Manager]",

      "employment_type": "[Full-Time, Part-Time, Temporary, Internship, Freelance, Volunteer, Apprenticeship, Side Project, Postdoctoral]",

      "employment_sector": "[Industry, Academic, Self-Employed]"

    }

    // Additional assessments for other positions go here

  ]

}

 

Job Function Guidelines:

 

{"job_function_guidelines": [{"function_name": "Data Scientist"},{"function_name": "Machine Learning Engineer"},{"function_name": "MLOps Engineer"},{"function_name": "Machine Learning Researcher"},{"function_name": "Data Engineer"},{"function_name": "AI Engineer"},{"function_name": "Generative AI Engineer"},{"function_name": "Data Architect"},{"function_name": "Database Administrator"},{"function_name": "Data Analyst"},{"function_name": "Business Analyst"},{"function_name": "BI Developer"},{"function_name": "Data Analytics"},{"function_name": "Economist"},{"function_name": "Bioinformatician"},{"function_name": "Biostatistician"},{"function_name": "Statistician"},{"function_name": "Quantitative Researcher"},{"function_name": "DevOps Engineer"},{"function_name": "QA / Software Tester"},{"function_name": "Frontend Software Engineer"},{"function_name": "Backend Software Engineer"},{"function_name": "Accounting"},{"function_name": "Administrative"},{"function_name": "Arts and Design"},{"function_name": "Business Development"},{"function_name": "Community and Social Services"},{"function_name": "Education"},{"function_name": "Engineering"},{"function_name": "Engineering Manager"},{"function_name": "Entrepreneurship"},{"function_name": "Finance"},{"function_name": "Healthcare Services"},{"function_name": "Human Resources"},{"function_name": "Information Technology"},{"function_name": "Legal"},{"function_name": "Marketing"},{"function_name": "Media and Communication"},{"function_name": "Military and Protective Services"},{"function_name": "Operations"},{"function_name": "Product Management"},{"function_name": "Program and Project Management"},{"function_name": "Purchasing"},{"function_name": "Quality Assurance"},{"function_name": "Real Estate"},{"function_name": "Research"},{"function_name": "Sales"},{"function_name": "Strategy"},{"function_name": "Support"},{"function_name": "Biotechnology"},{"function_name": "Materials Science and Engineering"},{"function_name": "Hardware and Electronics Engineering"},{"function_name": "Mechanical Engineering"},{"function_name": "Systems Design"},{"function_name": "Network and Computer Systems Administration"},{"function_name": "Software Architect"},{"function_name": "Cloud Engineer"},{"function_name": "Network Engineer"},{"function_name": "Security Engineer"},{"function_name": "DevSecOps Engineer"},{"function_name": "Technical Support Specialist"},{"function_name": "Web Development and Design"},{"function_name": "User Experience (UX) Designer"},{"function_name": "User Interface (UI) Designer"},{"function_name": "Human-Computer Interaction (HCI) Researcher"},{"function_name": "Natural Language Processing (NLP) Engineer"},{"function_name": "Computer Vision Engineer"},{"function_name": "Data Science Educator"},{"function_name": "Data Governance Analyst"},{"function_name": "Data Quality Analyst"},{"function_name": "DataOps Engineer"},{"function_name": "Ethical AI Specialist"},{"function_name": "AI Safety Engineer"},{"function_name": "Finance and Risk Analysis"},{"function_name": "Quantitative Analyst (Financial Industry)"},{"function_name": "Risk Analyst"},{"function_name": "Technical Recruiter"},{"function_name": "N/A"}]}

 

 

 

Additional Analysis Guidelines:

The job title is pivotal for selecting job functions, especially in the absence of a detailed job description.

Analysis extends beyond job titles to encompass the context of any job descriptions provided, focusing on specific duties and responsibilities for a comprehensive assessment.

In cases of ambiguous titles like 'Technical Lead', 'Consultant', 'Technical Advisor', 'Investigator', 'Researcher', etc., a thorough examination of job descriptions, additional responsibilities, and previous work experiences is essential for accurate function identification.

When clarity in job descriptions or titles is lacking, decisions will be informed by the candidate's overall professional background, field of education, and the context of the industry involved.

"""

    industry_experience = """Role: As a technical recruiter, evaluate a candidate's industry experience based on their resume (‘resume_text’ and/or ‘linkedin_text’) and past employers' descriptions (‘company_description’). Use the ‘IndustryList’ below to accurately align the candidate's background with specific industry criteria. For every role in the resume, including multiple positions at the same company, assess each job title independently to comprehensively capture the candidate's industry experience across all roles.

Instructions:

1 - Interpreting role context with company insights: Use 'company_description' for clarity when ‘resume_text’ and/or ‘linkedin_text’ lacks detail about role descriptions and industries. This background reveals the company’s sector and offerings, providing clues to a candidate's industry exposure. For instance, a "Data Scientist" role gains specificity if the company is known for Cybersecurity, suggesting relevant industry experience. This approach ensures accurate evaluations of a candidate's exposure to specific industries, especially when their roles are broadly defined.

2- Pay special attention to the context of each role for a nuanced assessment; for example, an IT support position at a bank may not showcase finance industry knowledge, whereas developing financial software at a tech firm likely indicates profound industry expertise.

3- In assessing ‘overall_industry_experience’, prioritize the candidate's latest industry role if they have over one year of experience there. Also, sum up the experience from all positions to gauge their total industry involvement, highlighting both current specialization and overall breadth of experience.

4- For recent graduates, evaluate university projects to infer industry interests and knowledge. For candidates with more than four years since graduation, prioritize professional experiences, treating academic projects as supplementary.

5- When evaluating roles with technical keywords (e.g., data science, AI) in non-technical contexts, assess them based on the industry they primarily serve, not the skillset. For example, a "Recruiter Data Science" role aligns with the Recruitment/HR industry, not Technology.

6- For each role, identify and assign up to two most relevant industries, ensuring high confidence in these selections. For the ‘overall_industry_experience’, provide assessments for up to three distinct industries, detailing the industry name and experience score for each.

Scoring Guideline (1-5):

No Exposure (1): No evidence of industry experience or relevance to the role.

Possible Exposure (2): Minimal indications of industry involvement; the connection is speculative.

Likely Exposure (3): Some evidence suggests industry experience, but multiple industries are plausible, or the assessment is largely based on inference.

Clear Exposure (4): Strong indicators of industry experience are present. Either the job description explicitly mentions relevant tasks or, in its absence, the role's industry is clear from the context, though not detailed.

Definitive Exposure (5): Over one year of experience within the main industry of the job, with clear and explicit mention of industry-relevant tasks in the job description.

{

  "IndustryList": [

    "Advertising", "Aerospace", "Agriculture", "Agritech", "Apparel & Fashion",

    "Artificial Intelligence (AI)", "Arts & Crafts", "Augmented Reality (AR)", "Automotive", "Banking",

    "Big Data", "Biotech", "Blockchain", "Clean Tech", "Cloud Computing", "Construction",

    "Consumer Electronics", "Consumer Goods", "Cybersecurity", "Data Analytics", "Data Storage",

    "Dating", "Defense", "Digital Marketing", "Digital Payments", "Drug Development", "E-commerce",

    "Edtech", "Education", "Energy", "Enterprise Software", "Entertainment", "Environmental",

    "Finance", "Fintech", "Fitness & Wellness", "Food & Beverage", "Gaming", "Genomics",

    "Government", "Hardware", "Healthcare", "Healthtech", "Hospitality", "Human Resources & Careers",

    "IAAS (Infrastructure as a Service)", "Industrial Automation", "Information Technology (IT)", "Insurance",

    "Insurtech", "Internet of Things (IoT)", "Legal", "Logistics & Supply Chain", "Management Consulting",

    "Manufacturing", "Marine Tech", "Marketing & Sales", "Media", "Nanotechnology", "Network Security",

    "Networking & Infrastructure", "News & Publishing", "Non-Profit", "Oil & Gas", "PAAS (Platform as a Service)",

    "Pharmaceuticals", "Professional Services", "Public Safety", "Quantum Computing", "Real Estate",

    "Renewable Energy", "Research", "Retail", "Robotics", "SAAS (Software as a Service)", "Security & Safety",

    "Semiconductor", "Social Media", "Software Development", "Sports", "Telecommunications",

    "Transportation & Logistics", "Utilities", "Venture Capital", "Virtual Reality (VR)", "VR & AR",

    "Wearables", "Cryptocurrency"

  ]

}

Output Format (JSON Only):

{

  "industry_analysis": [

    {

      "job": "[Job Title] at [Company]",

      "industry": ["[Industry 1]", "[Industry 2]"]

    }

// Additional positions until you have all the positions mentioned

  ],

  "overallExp": [

    {

      "overal_industry": ["[Industry 1]", "[Industry 2]", "[Industry 3]"],

      "score": ["[Score 1]", "[Score 2]", "[Score 3]"]

    }

  ]

}"""
    domain_categorization = """Objective: As a technical recruiter, you're tasked with evaluating a candidate's expertise in their technical domain based on their resume (‘resume_text’ and/or ‘linkedin_text’) and present/past employers' descriptions (‘company_description’). Your goal is to identify the primary technical domain and up to three subdomains they have experience in, guided by their job responsibilities and the nature of their past employment.

Instruction:

Context Considerations: Pay close attention to the industry context, the technologies the candidate has worked with, and the scale and scope of their projects. 

Domain and Subdomain Guidelines: Refer to the provided list of domain categories to guide your analysis. Each main domain includes specific subdomains representing more detailed expertise. Stick to this list for your domain and subdomain selections.

Exclusion of Non-Technical Roles: Do not include roles that are not technically oriented or where the technical aspects are not clear. Focus solely on positions where the candidate's technical skills and knowledge are directly applied.

Consolidated Domain Categories:

{

  "Domains": {

    "Data Analytics": {

      "Subdomains": [

        "Visualization",

        "Statistical Analysis",

        "Data Cleaning and Wrangling",

        "Geospatial Analysis",

        "Time Series Analysis",

        "Sentiment Analysis",

        "Marketing Analytics",

        "Predictive Modeling",

        "ETL"

      ]

    },

    "Data Scientist": {

      "Subdomains": [

        "Hypothesis Testing",

        "Time Series Analysis",

        "Anomaly Detection",

        "Sentiment Analysis",

        "Causal Inference",

        "Bayesian Statistics",

        "Regression Analysis",

        "Principal Component Analysis (PCA)",

        "Recommendation Systems",

        "Fraud Detection",

        "Churn Prediction",

        "Customer Segmentation",

        "Simulations",

        "Price Optimization Models",

        "Cybersecurity",

        "Natural Language Processing",

        "Statistical Analysis",

        "Optimization",

        "Feature Engineering",

        "Automated Machine Learning",

        "Decision Trees",

        "Random Forests",

        "Neural Networks"

      ]

    },

    "Machine Learning Engineer": {

      "Subdomains": [

        "Deep Learning",

        "Computer Vision",

        "Natural Language Processing",

        "Reinforcement Learning",

        "Neural Networks",

        "Decision Trees",

        "Random Forests",

        "Optimization",

        "Autonomous Systems",

        "Algorithmic Trading",

        "Robot Control",

        "Automated Machine Learning",

        "Chatbot",

        "Quantum Computing",

        "Real-time ML",

        "Collaborative Filtering",

        "Signal Processing",

        "Cybersecurity",

        "Sensor Fusion"

      ]

    },

    "MLOps Engineer": {

      "Subdomains": [

        "ML-Ops",

        "Continuous Integration/ Deployment (CI/CD)",

        "Containerization",

        "Cloud Computing",

        "Distributed Computing",

        "DevOps Practices",

        "Data Lifecycle Management",

        "Cloud Security",

        "Deploying ML Models"

      ]

    },

    "Machine Learning Researcher": {

      "Subdomains": [

        "Deep Learning",

        "Natural Language Processing",

        "Computer Vision",

        "Reinforcement Learning",

        "Bayesian Statistics",

        "Semantic Segmentation",

        "Object Detection",

        "Image Recognition",

        "Natural Language Generation (NLG)",

        "Quantum Machine Learning",

      ]

    },

    "Data Engineer, ML": {

      "Subdomains": [

        "Data Pipelines",

        "Feature Engineering",

        "Data Cleaning and Wrangling",

        "ML-Ops",

        "Database Management",

        "Cloud Computing",

        "Distributed Computing",

        "Edge Computing",

"Deploying ML Models"

        "Graph Databases"

      ]

    },

    "Data Engineer, Big Data": {

      "Subdomains": [

        "Big Data Analytics",

        "Distributed Computing",

        "Cloud Computing",

        "ETL",

        "Data Lifecycle Management",

        "Data Cleaning and Wrangling",

        "Database Management",

        "High-performance Computing (HPC)",

        "Data Governance",

        "Data Quality Management"

      ]

    },

    "Data Engineer, software": {

      "Subdomains": [

        "Software Development Practices",

        "Continuous Integration/Continuous Deployment (CI/CD)",

        "Database Management",

        "Data Security, Compliance, and Privacy",

        "Cloud Computing",

        "Microservices Architecture",

        "Data Lifecycle Management",

        "Network Architecture",

        "Data Governance",

        "Data Quality Management"

      ]

    },

    "AI Engineer": {

      "Subdomains": [

        "Machine Learning Models",

        "Deep Learning",

        "Natural Language Processing",

        "Computer Vision",

        "Model Optimization",

        "AI Ethics and Bias Mitigation",

        "Model Deployment",

        "Model Monitoring and Maintenance",

        "Reinforcement Learning",

        "Generative Models"

      ]

    },

    "Generative AI Engineer": {

      "Subdomains": [

        "Generative Adversarial Networks (GANs)",

        "Variational Autoencoders (VAEs)",

        "Transformer Models",

        "Text-to-Image Generation",

        "Voice Synthesis",

        "Content Creation AI",

        "Style Transfer",

        "DeepFakes Detection",

        "Music Generation",

        "Creative AI Applications"

      ]

    },

    "Data Architect": {

      "Subdomains": [

        "Data Modeling",

        "Data Warehouse Design",

        "Data Lake Architecture",

        "Metadata Management",

        "Data Governance",

        "Master Management"

},

"DataOps Engineer": {

"Subdomains": [

"Data Pipeline Automation",

"Data Quality",

"Data Governance",

"Continuous Integration/Continuous Deployment for Data",

"Monitoring and Logging for Data Systems",

"Collaboration between Data Teams and Operations",

"Data Security and Compliance",

"Performance Optimization",

"Data Storage and Computing Scalability",

"Data Lifecycle Management"

]

},

"AI Safety Engineer": {

"Subdomains": [

"Risk Assessment",

"Safety-critical AI Systems",

"Incident Response for AI Systems",

"AI Security",

"Robustness and Reliability",

"Transparency and Explainability",

"Ethical Considerations",

"AI Governance",

"Safety by Design",

"Monitoring and Evaluation"

]

},

"Quantitative Analyst (Financial Industry)": {

"Subdomains": [

"Quantitative Trading Strategies",

"Risk Management",

"Derivatives Pricing",

"Financial Modeling",

"Statistical Analysis",

"Algorithmic Trading",

"Portfolio Optimization",

"Econometrics",

"Machine Learning in Finance",

"Market Microstructure Analysis"

]

},

Output format: Document your findings using the following JSON structure for each position:

{ "domain_analysis": [ { "job": "[Job Title] at [Company Name]", "identified_domain": "[Domain]", "subdomain": [ "[Subdomain 1]", "[Subdomain 2]", "[Subdomain 3]" ] } // Repeat for each additional position ]}"""