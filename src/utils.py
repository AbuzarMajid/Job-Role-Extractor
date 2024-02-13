from openai import OpenAI
from src.logger import logging
from src.exceptions import CustomExcetions
import sys
import json
import re

def create_run(client: OpenAI, thread_id, assistant_id):
        try:
            run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id)
            logging.info('Successfully Created Run')
            return run
        except Exception as e:
            raise CustomExcetions(e, sys)
        

def assistant_definition(client: OpenAI, model_name, instructions):
    try:
        # defining assisatnt for the category in which the job description is given
        assistant = client.beta.assistants.create(
            instructions=instructions,
            name="Job Role Extractor",
            model=model_name
        )
        assistant_id = assistant.id
        logging.info('Assistant defined')
        #defining a thread for that assistant
        thread = client.beta.threads.create()
        thread_id = thread.id
        logging.info('Thread defined')
        return thread_id, assistant_id
    
    except Exception as e:
        raise CustomExcetions(e, sys)


def retrieve_run(client: OpenAI, thread_id, run_id):
    try:
        run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id)
        logging.info("successfully retrieved run")
        return run
    except Exception as e:
        raise CustomExcetions(e, sys)
    
def create_messages(client:OpenAI, thread_id, content):
    try:
        message = client.beta.threads.messages.create(
        thread_id= thread_id,
        role="user",
        content=content
        )
        logging.info("successfully defined message")
        return message

    except Exception as e:
        raise e
    
def show_messages(client: OpenAI, thread_id):
    try:
        messages = client.beta.threads.messages.list(
        thread_id= thread_id)
        response = messages.data[0].content[0].text.value
        logging.info('Successfully retrieved message')
        return response
    except Exception as e:
        raise CustomExcetions(e, sys)
    
def chat_completion(client:OpenAI, content, model, prompt):
    try:
        response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {
            "role": "system",
            "content": content
            },
            {
            "role": "user",
            "content": content        
            }
        ],
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        return  json.loads(response.choices[0].message.content)
    except Exception as e:
        raise CustomExcetions(e, sys)

def transform(json_string: str):
    json_string = json_string
    # Use regular expression to extract content including the initial "```json\n" and ending "\n```"
    match = re.search(r'```json\n(.*)\n```', json_string, re.DOTALL)

    if match:
        extracted_content = match.group(1)
        return extracted_content
    else:
        return json.loads(json_string)
    

# def domain_categ(client:OpenAI, content):
#     response = client.chat.completions.create(
#     model="gpt-4",
#     messages=[
#         {
#         "role": "system",
#         "content": JobRoleExtractor().domain_categorization
#         },
#         {
#         "role": "user",
#         "content": content      
#         }
#     ],
#     temperature=0,
#     max_tokens=1000,
#     top_p=1,
#     frequency_penalty=0,
#     presence_penalty=0
#     )
#     return json.loads(response.choices[0].message.content)


# def job_role(client:OpenAI, content):
#     response = client.chat.completions.create(
#     model="gpt-3.5-turbo-1106",
#     response_format={"type": "json_object"},
#     messages=[
#         {
#         "role": "system",
#         "content": "\nRole: you are Mike, a technical recruiter helping hiring managers by extracting the Job Functions when provided with Candidates' resumes and companies he/she has worked in.\n\nTask: Your task is to ANALYZE the ‘resume_text’. You will determine the primary and secondary job functions for each position by considering the skills, technologies, job title, company nature and size, and common phrases associated with each job function. You have to give a JSON output. \n\nIn addition, you must adhere to the following specific job_function_guidelines:\n\n\n- When processing job titles and descriptions, the model will focus on the overarching role and department. If a position falls under recruitment, talent acquisition, HR, marketing, sales, or administration, it will be categorized as \"None of the above,\" irrespective of the presence of technical keywords like \"Data Science,\" \"Artificial Intelligence,\" \"Analytics,\" or \"AI.\"\n\n- Keyword Context Analysis: The model will analyze keywords within the context of the job role. Technical terms are to be considered secondary if the primary function of the role is non-technical (such as HR or sales). The model should discern whether such terms are core to the job function or merely indicative of industry knowledge or peripheral skills.\n\nJOB FUNCTIONS:\n\"job_function_guidelines\": [\n  {\n    \"function_name\": \"Data Analyst\",\n    \"skills\": [\"Data cleaning\", \"data visualization\", \"statistics\", \"reporting\", \"SQL\", \"basic programming (e.g., Python, R)\", \"business acumen\"],\n    \"technologies\": [\"Tableau\", \"PowerBI\", \"Excel\", \"SQL databases\", \"Python\", \"R\"],\n    \"common_phrases\": [\"data reports\", \"KPIs\", \"SQL queries\", \"dashboards\", \"historical data analysis\", \"business metrics\", \"decision making support\"]\n  },\n  {\n    \"function_name\": \"Business Analyst\",\n    \"skills\": [\"Business acumen\", \"data analysis\", \"communication\", \"process improvement\", \"SQL\", \"basic data visualization\"],\n    \"technologies\": [\"Excel\", \"SQL\", \"Tableau\", \"PowerBI\"],\n    \"common_phrases\": [\"business process\", \"requirements gathering\", \"business strategy\", \"KPIs\", \"stakeholder communication\"]\n  },\n  {\n    \"function_name\": \"BI Developer\",\n    \"skills\": [\"Data visualization\", \"SQL\", \"data warehousing\", \"business acumen\", \"ETL processes\"],\n    \"technologies\": [\"Tableau\", \"PowerBI\", \"SQL databases\"],\n    \"common_phrases\": [\"dashboards\", \"data reports\", \"data warehouse\", \"ETL\", \"business metrics\"]\n  },\n  {\n    \"function_name\": \"Data Analytics\",\n    \"skills\": [\"Data cleaning\", \"data visualization\", \"statistics\", \"reporting\", \"SQL\", \"basic programming (e.g., Python, R)\", \"predictive analytics\", \"business acumen\", \"understanding of machine learning concepts\"],\n    \"technologies\": [\"Tableau\", \"PowerBI\", \"Excel\", \"SQL databases\", \"Python\", \"R\", \"ML libraries (e.g., scikit-learn, pandas, numpy)\"],\n    \"common_phrases\": [\"Predictive analytics\", \"SQL queries\", \"dashboards\", \"business metrics\", \"decision-making support\", \"ML concepts\", \"working with ML models\", \"data-driven insights\", \"statistical analysis\"]\n  },\n  {\n    \"function_name\": \"Data Scientist\",\n    \"skills\": [\"Advanced statistics\", \"machine learning\", \"deep learning\", \"data cleaning\", \"data visualization\", \"programming (e.g., Python, R)\", \"SQL\", \"hypothesis testing\", \"natural language processing (NLP)\", \"computer vision\", \"A/B testing\", \"stakeholder communication\", \"presentation of results\"],\n    \"technologies\": [\"Python\", \"R\", \"TensorFlow\", \"PyTorch\", \"Jupyter notebooks\", \"SQL databases\", \"cloud platforms (e.g., AWS, Google Cloud, Azure)\", \"ML libraries (e.g., scikit-learn, pandas, numpy)\"],\n    \"common_phrases\": [\"predictive modeling\", \"machine learning\", \"deep learning\", \"AI\", \"NLP\", \"computer vision\", \"unsupervised learning\", \"supervised learning\", \"reinforcement learning\", \"recommendation systems\", \"feature engineering\", \"model training and validation\"]\n  },\n\n {\n    \"function_name\": \"Machine Learning Engineer\",\n    \"skills\": [\"Machine learning\", \"deep learning\", \"programming languages like Python, Pyspark, Java, Scala, C++\", \"big data platforms\", \"distributed computing\", \"cloud computing\", \"SQL\", \"software engineering practices\", \"containerization\"],\n    \"technologies\": [\"Python\", \"TensorFlow\", \"PyTorch\", \"Jupyter notebooks\", \"Hadoop\", \"Spark\", \"Kubernetes\", \"Docker\", \"cloud platforms (AWS, Google Cloud, Azure)\", \"SQL databases\", \"Git\"],\n    \"common_phrases\": [\"ML model deployment\", \"ML pipelines\", \"scalable ML\", \"MLOps\", \"real-time data processing\", \"big data\", \"AI software\", \"deep learning\", \"NLP\", \"computer vision\", \"reinforcement learning\", \"LLMs\", \"CI/CD\", \"Docker\", \"Kubernetes\"]\n  },\n  {\n    \"function_name\": \"MLOps Engineer\",\n    \"skills\": [\"Machine learning model development and deployment\", \"CI/CD pipelines\", \"software engineering practices\", \"containerization and orchestration tools\", \"cloud computing and distributed systems\", \"big data technologies and databases\", \"programming languages such as Python\"],\n    \"technologies\": [\"Machine Learning libraries and frameworks (TensorFlow, PyTorch)\", \"containerization tools (Docker, Kubernetes)\", \"cloud platforms (AWS, Google Cloud, Azure)\", \"CI/CD tools (Jenkins, GitLab CI, CircleCI)\", \"monitoring tools (Prometheus, Grafana)\", \"data storage and processing (SQL databases, NoSQL databases, Spark)\", \"version control systems (Git)\"],\n    \"common_phrases\": [\"Machine learning model deployment\", \"continuous integration and continuous deployment (CI/CD)\", \"model monitoring and validation\", \"scalable machine learning\", \"infrastructure as code\", \"cloud-native ML solutions\", \"data pipeline automation\", \"model lifecycle management\"]\n  },\n  {\n    \"function_name\": \"Machine Learning Researcher\",\n    \"skills\": [\"Advanced knowledge of machine learning algorithms and principles\", \"deep learning\", \"natural language processing\", \"computer vision\", \"reinforcement learning\", \"data analysis\", \"advanced mathematics\", \"strong programming skills in Python, R\"],\n    \"technologies\": [\"Python\", \"R\", \"TensorFlow\", \"PyTorch\", \"Jupyter notebooks\", \"ML libraries (e.g., scikit-learn, pandas, numpy)\"],\n    \"common_phrases\": [\"developing and experimenting with novel machine learning algorithms\", \"conducting advanced research in areas like deep learning, natural language processing (NLP), and computer vision\", \"publishing findings in academic journals\", \"engaging in advanced statistical analysis and mathematical modeling\", \"exploring reinforcement learning techniques\", \"collaborating with both academic and industrial research teams\", \"developing prototypes using Python and R\", \"utilizing frameworks like TensorFlow and PyTorch for in-depth deep learning research\"]\n  },\n  {\n    \"function_name\": \"Data Engineer (with ML focus)\",\n    \"skills\": [\"Data pipeline construction\", \"data storage and retrieval\", \"knowledge of machine learning algorithms\", \"knowledge of deploying ML models in production\", \"cloud computing\", \"distributed systems\", \"SQL\", \"programming (e.g., Python, Java, Scala, Bash/Shell Scripting, C++)\"],\n    \"technologies\": [\"Spark\", \"AWS\", \"Google Cloud\", \"Azure\", \"SQL databases\", \"NoSQL databases\", \"Python\", \"TensorFlow\", \"PyTorch\", \"Docker\", \"Kubernetes\"],\n    \"common_phrases\": [\"data pipeline\", \"data storage\", \"data processing\", \"cloud platforms\", \"machine learning model deployment\", \"scalable ML\"]\n  },\n  {\n    \"function_name\": \"Data Engineer (with Big Data focus)\",\n    \"skills\": [\"Big data handling\", \"data pipeline construction\", \"ETL\", \"data storage and retrieval\", \"distributed systems\", \"SQL\", \"programming (e.g., Python, Spark, Java)\"],\n    \"technologies\": [\"Apache Hadoop Ecosystem (Hive, Pig, HBase, etc.)\", \"Spark\", \"AWS\", \"Google Cloud\", \"Azure\", \"SQL databases\", \"NoSQL databases\", \"Python\"],\n    \"common_phrases\": [\"big data\", \"data pipeline\", \"data storage\", \"data processing\", \"ETL\", \"cloud platforms\", \"distributed systems\"]\n  },\n  {\n    \"function_name\": \"Data Engineer (with software engineering focus)\",\n    \"skills\": [\"Strong software engineering practices (version control, testing, CI/CD)\", \"API development\", \"data pipeline construction\", \"performance optimization\", \"cloud computing\", \"distributed systems\", \"knowledge of SQL and NoSQL databases\", \"programming (e.g., Python, Java, Scala, Go)\"],\n    \"technologies\": [\"Git\", \"Docker\", \"Kubernetes\", \"AWS\", \"Google Cloud\", \"Azure\", \"SQL databases\", \"NoSQL databases (like MongoDB, Cassandra)\", \"Python\", \"Java\", \"Scala\", \"RESTful APIs\"],\n    \"common_phrases\": [\"software development practices\", \"API integration\", \"data pipeline optimization\", \"cloud-native solutions\", \"distributed computing\", \"containerization\", \"performance tuning\", \"data streaming\"]\n  },\n  {\n    \"function_name\": \"Data Architect\",\n    \"skills\": [\"Data modeling\", \"system design\", \"knowledge of various database technologies (SQL and NoSQL)\", \"big data technologies\", \"data governance\", \"ETL processes\", \"data security\", \"understanding of machine learning concepts\", \"cloud computing architectures\", \"understanding of distributed systems\"],\n    \"technologies\": [\"SQL databases\", \"NoSQL databases\", \"big data tools (Hadoop, Spark)\", \"cloud platforms (AWS, Google Cloud, Azure)\", \"data modeling tools\"],\n    \"common_phrases\": [\"data modeling\", \"database design\", \"data warehousing\", \"big data architecture\", \"data governance\", \"cloud data solutions\", \"data security\", \"scalable data architecture\"]\n  },\n  {\n    \"function_name\": \"Database Administrator\",\n    \"skills\": [\"SQL\", \"database systems management\", \"backup and recovery\", \"security\", \"performance tuning\"],\n    \"technologies\": [\"SQL databases\", \"NoSQL databases\", \"Oracle\", \"Microsoft SQL Server\"],\n    \"common_phrases\": [\"database management\", \"database performance\", \"database security\", \"backup and recovery\"]\n  },\n\n  {\n    \"function_name\": \"Statistician\",\n    \"skills\": [\"Advanced statistics\", \"hypothesis testing\", \"predictive modeling\", \"data visualization\", \"programming (e.g., R, Python)\"],\n    \"technologies\": [\"R\", \"Python\", \"Excel\", \"Tableau\"],\n    \"common_phrases\": [\"statistical modeling\", \"statistical analysis\", \"hypothesis testing\", \"predictive modeling\"]\n  },\n  {\n    \"function_name\": \"None of the above\",\n    \"skills\": [],\n    \"technologies\": [],\n    \"common_phrases\": []\n  }\n]\n\nOutput Format: (Strictly follow it)\nEach dictionary should represent one position and so on.\n{\"job_role_functions\":{\n\"job_title\": \"[Job Title]\",\n\"company_name\": \"[Company Name]\",\n\"primary_function\": \"[Primary Job Function]\",\n\"secondary_function\": \"[Secondary Job Function]\",\n\"function_distribution\": \"[Distribution between primary and secondary job functions like 50% ML 50% data science]\"\n}{\n....\n}}\n\nUnless provided with resume you will not respond to anything\n\n\n"
#         },
#         {
#         "role": "user",
#         "content": content
#         }
#     ],
#     temperature=0,
#     max_tokens=1216,
#     top_p=1,
#     frequency_penalty=0,
#     presence_penalty=0
#     )
#     return json.loads(response.choices[0].message.content)


