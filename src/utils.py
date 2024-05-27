from openai import OpenAI
from src.logger import logging
from src.exceptions import CustomExcetions
import sys
import json
from datetime import datetime
import aiohttp

def create_completion(client: OpenAI, model_name, messages):
    try:
        logging.info('Entered Compeltion')
        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.0,
            max_tokens=3000
        )
        logging.info('Done with completion')
        response = completion.choices[0].message
        return response.content
    except Exception as e:
        raise CustomExcetions(e, sys)
    

def create_chat_completion(client: OpenAI, model_name, messages):
    try:
        logging.info('Entered Compeltion')
        completion = client.chat.completions.create(
            model=model_name,
            response_format={"type": "json_object"},
            messages=messages,
            temperature=0.0,
            max_tokens=3000
        )
        logging.info(f'Done with completion')
        response = completion.choices[0].message
        return json.loads(response.content)
    except Exception as e:
        raise "Error in creating chat completion : {}" .format(e)


def response_formatter(resume_information: dict, job_functions: bool, domain_categorization: bool, industry_experience: bool, education: bool):
    try:
        # when job function is true

        if job_functions:
            profile_analysis = []
            num_job_functions = len(resume_information["resume_information"]['job_functions'])
            for i in range(num_job_functions):
                profile = {}
                job_function = resume_information["resume_information"]['job_functions'][i]

                profile['job_title'] = job_function.get('job_title', None)
                profile['date_range'] = job_function.get('date_range', None)
                profile['company_id'] = job_function.get('company_id', None)
                profile['primary_function'] = job_function.get('primary_function', None).replace("N/A", "")
                profile['secondary_function'] = job_function.get('secondary_function', None).replace("N/A", "")
                profile['seniority_level'] = job_function.get('seniority_level', None)
                profile['role_hierarchy'] = job_function.get('role_hierarchy', None)
                profile['employment_type'] = job_function.get('employment_type', None)
                profile['employment_sector'] = job_function.get('employment_sector', None)

                if industry_experience:    
                    industry_info = next((industry for industry in resume_information["resume_information"]['industry_analysis'] if industry["job_title"] == job_function["job_title"]), {"industry": ""})
                    profile['industry'] = industry_info.get('industry', "")    
            
                if domain_categorization:
                    domain_info = next((domain for domain in resume_information["resume_information"]['domain_analysis'] if domain["job_title"] == job_function["job_title"]), {"identified_domain": "", "subdomain": ""})
                    profile['domain'] = domain_info.get('identified_domain', "")
                    profile['subdomain'] = domain_info.get('subdomain', "")

                if any(profile.values()):
                    profile_analysis.append(profile)

            # Check if overall experience information exists
            if industry_experience:
                if resume_information["resume_information"]['overallExp']:
                    overall_exp_dict = resume_information["resume_information"]['overallExp'][0]
                    profile_analysis.append(overall_exp_dict)
            
            if education:
                if resume_information["resume_information"]['educations']:
                    education = resume_information["resume_information"]['educations']
                    profile_analysis.append({"educations": education})

            return {"profile_analysis": profile_analysis}
        
        # when job function and is false and industry expereince and domain categorization is true
        elif industry_experience and domain_categorization: 
            num_industry_experience = len(resume_information["resume_information"]['industry_analysis'])
            profile_analysis = []

            for  i in range(num_industry_experience):
                profile = {}  
                industry_experience_info = resume_information["resume_information"]['industry_analysis'][i]
                
                profile['job_title'] = industry_experience_info.get('job_title', None)
                profile['date_range'] = industry_experience_info.get('date_range', None)
                profile['company_id'] = industry_experience_info.get('company_id', None)
                profile['industry'] = industry_experience_info.get('industry', None)
            
                if domain_categorization:
                    domain_info = next((domain for domain in resume_information["resume_information"]['domain_analysis'] if domain["job"] == industry_experience_info["job"]), {"identified_domain": "", "subdomain": ""})
                    profile['domain'] = domain_info.get('identified_domain', "")
                    profile['subdomain'] = domain_info.get('subdomain', "")

                if any(profile.values()):
                    profile_analysis.append(profile)

                # Check if overall experience information exists
            if resume_information["resume_information"]['overallExp']:
                overall_exp_dict = resume_information["resume_information"]['overallExp'][0]
                profile_analysis.append({"overall experience": overall_exp_dict})

            if education:
                if resume_information["resume_information"]['educations']:
                    education = resume_information["resume_information"]['educations']
                    profile_analysis.append({"educations": education})

            return {"profile_analysis": profile_analysis}
        
        # when domain categroizatrion is true only
        elif domain_categorization and education:
            return {"Domain Categorizaton": resume_information["resume_information"]["domain_analysis"], "educations": resume_information["resume_information"]["educations"]}

        elif industry_experience and education:
            return {"Industry Experience": resume_information["resume_information"]["industry_analysis"], "educations": resume_information["resume_information"]["educations"]}

        elif domain_categorization:
            return {"Domain Categorizaton": resume_information["resume_information"]["domain_analysis"]}
        
        # when industry expeirience is try only
        elif industry_experience:
            return {"Industry Experience": resume_information["resume_information"]["industry_analysis"]}
        
        elif education:
            return {"Industry Experience": resume_information["resume_information"]["educations"]}

        if not (job_functions or domain_categorization or industry_experience or education):
            return{"message": "At least one of the options (job_functions, domain_categorization, industry_experience) must be True."}
        
    except Exception as e:
        raise CustomExcetions(e, sys)

def check_overlap_all(roles):
    overlaps = []
    for i in range(len(roles)):
        for j in range(i+1, len(roles)):
            try:        
                role1 = roles[i]
                role2 = roles[j]
                # Convert date ranges to datetime objects
                start_date1, end_date1 = convert_date_range(role1['date_range'])
                start_date2, end_date2 = convert_date_range(role2['date_range'])

                # Check for overlap
                if start_date1 <= end_date2 and start_date2 <= end_date1:
                    overlap_start = max(start_date1, start_date2)
                    overlap_end = min(end_date1, end_date2)
                    overlap_period = (overlap_end.year - overlap_start.year) * 12 + overlap_end.month - overlap_start.month + 1
                    if overlap_period > 1:
                        overlaps.append({"role_1": role1['job_title'], "role_2": role2['job_title'], "month": overlap_period})
            except:
                continue
    return overlaps

def convert_date_range(date_range):
    if "present" in date_range.lower():
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date_range.split(' - ')[1], '%b %Y')
    start_date = datetime.strptime(date_range.split(' - ')[0], '%b %Y')
    return start_date, end_date


def matching_experience(request, prompt_response):
    # Extract job titles from prompt response
    # print(prompt_response)
    job_titles = [experience["job_title"] for experience in prompt_response["profile_analysis"] if experience.get("job_title")]
    # print(job_titles)
    job_title_presence = {}

    # Iterate through job titles in the request
    for experiences in request["data"]["experiences"]:
        # print(f"experience:{experiences}")
        # print(experiences["job_title"])
        job_title = experiences["title"]
        if job_title in job_titles:
            job_title_presence[job_title] = "present"
        else:
            job_title_presence[job_title] = "absent"

    return job_title_presence

def response_formatter_pdf(resume_information: dict, job_functions: bool, domain_categorization: bool, industry_experience: bool):
    try:
        # when job function is true

        if job_functions:
            profile_analysis = []
            num_job_functions = len(resume_information["resume_information"]['job_functions'])
            for i in range(num_job_functions):
                profile = {}
                job_function = resume_information["resume_information"]['job_functions'][i]

                profile['job_title'] = job_function.get('job_title', None)
                profile['date_range'] = job_function.get('date_range', None)
                profile['company_id'] = job_function.get('company_id', None).replace("N/A", "")
                profile['primary_function'] = job_function.get('primary_function', None).replace("N/A", "")
                profile['secondary_function'] = job_function.get('secondary_function', None).replace("N/A", "")
                profile['seniority_level'] = job_function.get('seniority_level', None).replace("N/A", "")
                profile['role_hierarchy'] = job_function.get('role_hierarchy', None)
                profile['employment_type'] = job_function.get('employment_type', None)
                profile['employment_sector'] = job_function.get('employment_sector', None)

                if industry_experience:    
                    industry_info = next((industry for industry in resume_information["resume_information"]['industry_analysis'] if industry["job_title"] == job_function["job_title"]), {"industry": ""})
                    profile['industry'] = industry_info.get('industry', "")    
            
                if domain_categorization:
                    domain_info = next((domain for domain in resume_information["resume_information"]['domain_analysis'] if domain["job_title"] == job_function["job_title"]), {"identified_domain": "", "subdomain": ""})
                    profile['domain'] = domain_info.get('identified_domain', "")
                    profile['subdomain'] = domain_info.get('subdomain', "")

                if any(profile.values()):
                    profile_analysis.append(profile)

            # Check if overall experience information exists
            if industry_experience:
                if resume_information["resume_information"]['overallExp']:
                    overall_exp_dict = resume_information["resume_information"]['overallExp'][0]
                    profile_analysis.append(overall_exp_dict)
            

            return {"profile_analysis": profile_analysis}
        
        # when job function and is false and industry expereince and domain categorization is true
        elif industry_experience and domain_categorization: 
            num_industry_experience = len(resume_information["resume_information"]['industry_analysis'])
            profile_analysis = []

            for  i in range(num_industry_experience):
                profile = {}  
                industry_experience_info = resume_information["resume_information"]['industry_analysis'][i]
                
                profile['job_title'] = industry_experience_info.get('job_title', None)
                profile['date_range'] = industry_experience_info.get('date_range', None)
                profile['company_id'] = industry_experience_info.get('company_id', None)
                profile['industry'] = industry_experience_info.get('industry', None)
            
                if domain_categorization:
                    domain_info = next((domain for domain in resume_information["resume_information"]['domain_analysis'] if domain["job"] == industry_experience_info["job"]), {"identified_domain": "", "subdomain": ""})
                    profile['domain'] = domain_info.get('identified_domain', "")
                    profile['subdomain'] = domain_info.get('subdomain', "")

                if any(profile.values()):
                    profile_analysis.append(profile)

                # Check if overall experience information exists
            if resume_information["resume_information"]['overallExp']:
                overall_exp_dict = resume_information["resume_information"]['overallExp'][0]
                profile_analysis.append({"overall experience": overall_exp_dict})


            return {"profile_analysis": profile_analysis}
        
        # when domain categroizatrion is true only
        elif domain_categorization:
            return {"Domain Categorizaton": resume_information["resume_information"]["domain_analysis"]}
        
        # when industry expeirience is try only
        elif industry_experience:
            return {"Industry Experience": resume_information["resume_information"]["industry_analysis"]}
        
        if not (job_functions or domain_categorization or industry_experience):
            return{"message": "At least one of the options (job_functions, domain_categorization, industry_experience) must be True."}
        
    except Exception as e:
        raise CustomExcetions(e, sys)

def map_talent_info_pdf(final_dict, linkenin_text):
    merge_dicts = lambda x, y: {**x, **y}
    mapped_data_experience = [
    merge_dicts(
        company_data,
        next(
            (profile for profile in final_dict["profile_analysis"] 
             if profile.get("job_title") == company_data["title"]),
            {}
        )
    )
    for company_data in linkenin_text["data"]["experiences"]
    ]
    for each in mapped_data_experience:
        each.pop("job_title", None)

    linkenin_text["data"]["experiences"] = mapped_data_experience
    industries = final_dict["profile_analysis"][-1]["overal_industry"]
    score = final_dict["profile_analysis"][-1]["score"]
    industry_scores = {}

    # Map the experience lists together
    for i in range(len(industries)):
        industry_scores[industries[i]] = score[i]


    linkenin_text["overlapping_roles"] = check_overlap_all(final_dict["profile_analysis"])
    linkenin_text["mapping_info"] = matching_experience(request=linkenin_text, prompt_response=final_dict)

    linkenin_text["overall_experience"] = industry_scores
    return (linkenin_text)

def map_talent_info(final_dict, linkenin_text):
    merge_dicts = lambda x, y: {**x, **y}
    mapped_data_experience = [
    merge_dicts(
        company_data,
        next(
            (profile for profile in final_dict["profile_analysis"] 
             if profile.get("job_title") == company_data["title"] and profile.get("company_id") == company_data["company_id"]),
            {}
        )
    )
    for company_data in linkenin_text["data"]["experiences"]
    ]
    education_info = [each for profile in final_dict["profile_analysis"] if profile.get("educations") != None for each in profile.get("educations")]
    mapped_data_education = [
    merge_dicts(
        education_data,
        next(
            (profile for profile in education_info
             if profile.get("eduId") == education_data["eduId"] and profile.get("degree") == education_data["degree"]),
            {}
        )
    )
    for education_data in linkenin_text["data"]["educations"]
    ]
    for each in mapped_data_experience:
        each.pop("job_title", None)

    linkenin_text["data"]["experiences"] = mapped_data_experience
    linkenin_text["data"]["educations"] = mapped_data_education
    industries = final_dict["profile_analysis"][-2]["overal_industry"]
    score = final_dict["profile_analysis"][-2]["score"]
    industry_scores = {}

    # Map the experience lists together
    for i in range(len(industries)):
        industry_scores[industries[i]] = score[i]

    # Deleting the title key from final dictionery


    linkenin_text["overlapping_roles"] = check_overlap_all(final_dict["profile_analysis"])
    linkenin_text["mapping_info"] = matching_experience(request=linkenin_text, prompt_response=final_dict)

    linkenin_text["overall_experience"] = industry_scores
    return (linkenin_text)

async def call_api(
    url,
    data,
    api_key=None,
    headers=None,
    text=False,
    # timeout=None,
):
    headers = headers or {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # timeout = timeout or 60 * 1.5
    # client_timeout = aiohttp.ClientTimeout(
    #     total=None, sock_connect=timeout, sock_read=timeout
    # )
    async with aiohttp.ClientSession() as session:
        session = session.post(url=url, json=data, headers=headers) #timeout=client_timeout)
        async with session as response:
            response_text = ""
            try:
                response_status_code = response.status
                response_text = await response.text()
                if text:
                    return response_text #response_status_code
                response_json = json.loads(response_text)
                return json.loads(response_json["choices"][0]["message"]["content"])
            except:
                print("entry")
                return response_text, response_status_code
                    
def get_urls_and_headers(resume_text, companies_description, education_info):
    urls_and_data = [
                    ("https://api.openai.com/v1/chat/completions", {
                                    "model": "gpt-3.5-turbo-0125",
                                    "messages": [
                                        {
                                        "role": "system",
                                        "content": [
                                            {
                                            "text": "Role: You are a technical recruiter.\n\n \n\nTask: Your task is to ANALYZE the resume_text and/or linkedin_text. For each job position listed, you will:\n\n \n\nDetermine the primary and secondary job functions by considering the job title, job description, skills, technologies, company nature, and common phrases associated with each job function. Ensure to STRICTLY choose job functions from the job_function_guidelines list provided below. If no listed job functions apply, choose N/A.\n\n\n\nCategorize each position into one of three roles: Individual Contributor, Team Lead, or Manager, as defined in the Role Hierarchy Category.\n\nDetermine the Employment Type and Employment Sector for each role.\n\nSeniority Level:\n\nEntry Level: Description: Roles requiring minimal experience or aimed at recent graduates. Keywords often include \"Junior\", \"Assistant\", \"Trainee\", \"Intern\", \"Analyst\", and \"Coordinator\", \"Associate\".\nMid-Level: Positions requiring moderate experience and some leadership or specialized skills. Look for keywords like  \"Specialist\", and \"Supervisor\", \"Principal\"\nSenior: Roles demanding extensive experience and advanced skills, often with significant responsibilities. Common keywords include \"Senior\", \"Staff\", \"Expert\", and \"Advisor.\nTeam Lead: Roles involving guidance or influence over others, often requiring leadership and specialized expertise without direct management of staff. Keywords to identify these positions include \"Lead\", \"Subject Matter Expert\", \"mentored\", \"coaching\", and titles such as \"Lead\", \"Principal\", \"Sr. Principal\", \"Staff\", or \"Distinguished\".\nManager: Roles with direct management responsibilities, overseeing teams or departments, and involving strategic decision-making and leadership. These positions are identified by keywords like \"Manager\", \"P&L\".\nDirector: Senior management roles with significant strategic and operational responsibilities, often overseeing multiple departments or large teams, and participating in high-level decision-making. Look for keywords such as \"Director\", \"Head\", \"VP\" (in smaller organizations), \"Executive\", and \"Chief\" (if not C-level).\n\nRole Hierarchy Category:\n\nIndividual Contributor: Default category for roles not meeting criteria for Team Lead or Manager.\n\nTeam Lead: A role centered on guiding or influencing others without the responsibility of managing direct reports (keywords such as \"Lead\", \"Subject Matter Expert\", \"mentored\", or \"coaching\" or titles with \"Lead\", \"Principal\", \"Sr. Principal\", \"Staff\", or \"Distinguished\" often signify a Team Lead position).\n\nManager: Identified by having direct reports and keywords like \"Manager\", \"P&L\", “Director”, “Head” etc.\n\n \n\nEmployment Type:\n\nKeywords indicate whether the role is Full-Time, Part-Time, Temporary, Internship, Freelance, Volunteer, Apprenticeship, Side Project, or Postdoctoral.\n\n \n\nEmployment Sector:\n\nCategorized as Industry, Academic, or Self-Employed based on the description. The industry sector focuses on producing goods and services, while the academic field involves roles in education, emphasizing teaching, research and other scholarly activities. Self-employment covers terms like self-employed, owner, entrepreneur, freelancer, co-founder, entrepreneur, and CEO of small companies (under 10 people),\n\n \n\nOutput JSON format:\n\n{ \n\"job_functions\": [ \n{ \n\"job_title\": \"\",\n\"date_range\":\"\", \n\"company_id\": \"\", \n\"primary_function\": \"[Primary Job Function]\", \n\"secondary_function\": \"[Secondary Job Function]\",\n\"seniority_level\": \"[level: Entry Level, Mid Level, Senior, Team Lead, Manager, Director\"],\n\"role_hierarchy\": \"[Individual Contributor, Team Lead, Manager]\", \n\"seniority_level\": \n\"employment_type\": \"[Full-Time, Part-Time, Temporary, Internship, Freelance, Volunteer, Apprenticeship, Side Project, Postdoctoral]\", \n\"employment_sector\": \"[Industry, Academic, Self-Employed]\" \n}\n // Additional assessments for all other positions go here \n] \n}\n\n \n\nJob Function Guidelines:\n\n{\"job_function_guidelines\": [{\"function_name\": \"Data Scientist\"},{\"function_name\": \"Machine Learning Engineer\"},{\"function_name\": \"MLOps Engineer\"},{\"function_name\": \"Machine Learning Researcher\"},{\"function_name\": \"Data Engineer\"},{\"function_name\": \"AI Engineer\"},{\"function_name\": \"Generative AI Engineer\"},{\"function_name\": \"Data Architect\"},{\"function_name\": \"Database Administrator\"},{\"function_name\": \"Data Analyst\"},{\"function_name\": \"Business Analyst\"},{\"function_name\": \"BI Developer\"},{\"function_name\": \"Data Analytics\"},{\"function_name\": \"Economist\"},{\"function_name\": \"Bioinformatician\"},{\"function_name\": \"Biostatistician\"},{\"function_name\": \"Statistician\"},{\"function_name\": \"Quantitative Researcher\"},{\"function_name\": \"DevOps Engineer\"},{\"function_name\": \"QA / Software Tester\"},{\"function_name\": \"Frontend Software Engineer\"},{\"function_name\": \"Backend Software Engineer\"},{\"function_name\": \"Accounting\"},{\"function_name\": \"Administrative\"},{\"function_name\": \"Arts and Design\"},{\"function_name\": \"Business Development\"},{\"function_name\": \"Community and Social Services\"},{\"function_name\": \"Education\"},{\"function_name\": \"Engineering\"},{\"function_name\": \"Engineering Manager\"},{\"function_name\": \"Entrepreneurship\"},{\"function_name\": \"Finance\"},{\"function_name\": \"Healthcare Services\"},{\"function_name\": \"Human Resources\"},{\"function_name\": \"Information Technology\"},{\"function_name\": \"Legal\"},{\"function_name\": \"Marketing\"},{\"function_name\": \"Media and Communication\"},{\"function_name\": \"Military and Protective Services\"},{\"function_name\": \"Operations\"},{\"function_name\": \"Product Management\"},{\"function_name\": \"Program and Project Management\"},{\"function_name\": \"Purchasing\"},{\"function_name\": \"Quality Assurance\"},{\"function_name\": \"Real Estate\"},{\"function_name\": \"Research\"},{\"function_name\": \"Sales\"},{\"function_name\": \"Strategy\"},{\"function_name\": \"Support\"},{\"function_name\": \"Biotechnology\"},{\"function_name\": \"Materials Science and Engineering\"},{\"function_name\": \"Hardware and Electronics Engineering\"},{\"function_name\": \"Mechanical Engineering\"},{\"function_name\": \"Systems Design\"},{\"function_name\": \"Network and Computer Systems Administration\"},{\"function_name\": \"Software Architect\"},{\"function_name\": \"Cloud Engineer\"},{\"function_name\": \"Network Engineer\"},{\"function_name\": \"Security Engineer\"},{\"function_name\": \"DevSecOps Engineer\"},{\"function_name\": \"Technical Support Specialist\"},{\"function_name\": \"Web Development and Design\"},{\"function_name\": \"User Experience (UX) Designer\"},{\"function_name\": \"User Interface (UI) Designer\"},{\"function_name\": \"Human-Computer Interaction (HCI) Researcher\"},{\"function_name\": \"Natural Language Processing (NLP) Engineer\"},{\"function_name\": \"Computer Vision Engineer\"},{\"function_name\": \"Data Science Educator\"},{\"function_name\": \"Data Governance Analyst\"},{\"function_name\": \"Data Quality Analyst\"},{\"function_name\": \"DataOps Engineer\"},{\"function_name\": \"Ethical AI Specialist\"},{\"function_name\": \"AI Safety Engineer\"},{\"function_name\": \"Finance and Risk Analysis\"},{\"function_name\": \"Quantitative Analyst (Financial Industry)\"},{\"function_name\": \"Risk Analyst\"},{\"function_name\": \"Technical Recruiter\"},{\"function_name\": \"N/A\"}]}\n \n\n\nAdditional Analysis Guidelines:\n\nThe job title is pivotal for selecting job functions, especially in the absence of a detailed job description.\n\nAnalysis extends beyond job titles to encompass the context of any job descriptions provided, focusing on specific duties and responsibilities for a comprehensive assessment.\n\nIn cases of ambiguous titles like 'Technical Lead', 'Consultant', 'Technical Advisor', 'Investigator', 'Researcher', etc., a thorough examination of job descriptions, additional responsibilities, and previous work experiences is essential for accurate function identification.\n\nWhen clarity in job descriptions or titles is lacking, decisions will be informed by the candidate's overall professional background, field of education, and the context of the industry involved.\n\nMake sure to cover every position in the given experiences\n",
                                            "type": "text"
                                            }
                                        ]
                                        },
                                        {
                                        "role": "user",
                                        "content": [
                                            {
                                            "type": "text",
                                            "text": resume_text
                                            }
                                        ]
                                        }
                                    ],
                                    "temperature": 0,
                                    "max_tokens": 2000,
                                    "top_p": 1,
                                    "response_format": { "type": "json_object" },
                                    "frequency_penalty": 0,
                                    "presence_penalty": 0
                                    }),
                    ("https://api.openai.com/v1/chat/completions", {
                                    "model": "gpt-3.5-turbo-0125",
                                    "messages": [
                                        {
                                        "role": "system",
                                        "content": [
                                            {
                                            "text": "\"Role: As a technical recruiter, evaluate a candidate'\''s industry experience based on their resume (‘resume_text’ and/or ‘linkedin_text’) and past employers'\'' descriptions (‘company_description’). Use the ‘IndustryList’ below to accurately align the candidate'\''s background with specific industry criteria. For every role in the resume, including multiple positions at the same company, assess each job title independently to comprehensively capture the candidate'\''s industry experience across all roles.\n\nInstructions:\n\n1 - Interpreting role context with company insights: Use '\''company_description'\'' for clarity when ‘resume_text’ and/or ‘linkedin_text’ lacks detail about role descriptions and industries. This background reveals the company’s sector and offerings, providing clues to a candidate'\''s industry exposure. For instance, a \"Data Scientist\" role gains specificity if the company is known for Cybersecurity, suggesting relevant industry experience. This approach ensures accurate evaluations of a candidate'\''s exposure to specific industries, especially when their roles are broadly defined.\n\n2- Pay special attention to the context of each role for a nuanced assessment; for example, an IT support position at a bank may not showcase finance industry knowledge, whereas developing financial software at a tech firm likely indicates profound industry expertise.\n\n3- In assessing ‘overall_industry_experience’, prioritize the candidate'\''s latest industry role if they have over one year of experience there. Also, sum up the experience from all positions to gauge their total industry involvement, highlighting both current specialization and overall breadth of experience.\n\n4- For recent graduates, evaluate university projects to infer industry interests and knowledge. For candidates with more than four years since graduation, prioritize professional experiences, treating academic projects as supplementary.\n\n5- When evaluating roles with technical keywords (e.g., data science, AI) in non-technical contexts, assess them based on the industry they primarily serve, not the skillset. For example, a \"Recruiter Data Science\" role aligns with the Recruitment/HR industry, not Technology.\n\n6- For each role, identify and assign up to two most relevant industries, ensuring high confidence in these selections. For the ‘overall_industry_experience’, provide assessments for up to three distinct industries, detailing the industry name and experience score for each.\n\nScoring Guideline (1-5):\n\nNo Exposure (1): No evidence of industry experience or relevance to the role.\n\nPossible Exposure (2): Minimal indications of industry involvement; the connection is speculative.\n\nLikely Exposure (3): Some evidence suggests industry experience, but multiple industries are plausible, or the assessment is largely based on inference.\n\nClear Exposure (4): Strong indicators of industry experience are present. Either the job description explicitly mentions relevant tasks or, in its absence, the role'\''s industry is clear from the context, though not detailed.\n\nDefinitive Exposure (5): Over one year of experience within the main industry of the job, with clear and explicit mention of industry-relevant tasks in the job description.\n\nIndustry list:\n{ \"IndustryList\": [ \"Advertising\", \"Aerospace\", \"Agriculture\", \"Agritech\", \"Apparel & Fashion\", \"Artificial Intelligence (AI)\", \"Arts & Crafts\", \"Augmented Reality (AR)\", \"Automotive\", \"Banking\", \"Big Data\", \"Biotech\", \"Blockchain\", \"Clean Tech\", \"Cloud Computing\", \"Construction\", \"Consumer Electronics\", \"Consumer Goods\", \"Cybersecurity\", \"Data Analytics\", \"Data Storage\", \"Dating\", \"Defense\", \"Digital Marketing\", \"Digital Payments\", \"Drug Development\", \"E-commerce\", \"Edtech\", \"Education\", \"Energy\", \"Enterprise Software\", \"Entertainment\", \"Environmental\", \"Finance\", \"Fintech\", \"Fitness & Wellness\", \"Food & Beverage\", \"Gaming\", \"Genomics\", \"Government\", \"Hardware\", \"Healthcare\", \"Healthtech\", \"Hospitality\", \"Human Resources & Careers\", \"IAAS (Infrastructure as a Service)\", \"Industrial Automation\", \"Information Technology (IT)\", \"Insurance\", \"Insurtech\", \"Internet of Things (IoT)\", \"Legal\", \"Logistics & Supply Chain\", \"Management Consulting\", \"Manufacturing\", \"Marine Tech\", \"Marketing & Sales\", \"Media\", \"Nanotechnology\", \"Network Security\", \"Networking & Infrastructure\", \"News & Publishing\", \"Non-Profit\", \"Oil & Gas\", \"PAAS (Platform as a Service)\", \"Pharmaceuticals\", \"Professional Services\", \"Public Safety\", \"Quantum Computing\", \"Real Estate\", \"Renewable Energy\", \"Research\", \"Retail\", \"Robotics\", \"SAAS (Software as a Service)\", \"Security & Safety\", \"Semiconductor\", \"Social Media\", \"Software Development\", \"Sports\", \"Telecommunications\", \"Transportation & Logistics\", \"Utilities\", \"Venture Capital\", \"Virtual Reality (VR)\", \"VR & AR\", \"Wearables\", \"Cryptocurrency\" ] }\n\nOutput Format(JSON only):\n{ \"industry_analysis\": [ { \"job_title\": \"\", \"job\": \"[Job Title] at [Company]\", \"industry\": [\"[Industry 1]\", \"[Industry 2]\"] } // Additional positions until you have all the positions mentioned ], \"overallExp\": [ { \"overal_industry\": [\"[Industry 1]\", \"[Industry 2]\", \"[Industry 3]\"], \"score\": [\"[Score 1]\", \"[Score 2]\", \"[Score 3]\"] } ] }\n",
                                            "type": "text"
                                            }
                                        ]
                                        },
                                        {
                                        "role": "user",
                                        "content": [
                                            {
                                            "type": "text",
                                            "text": resume_text +"\n" + companies_description
                                            }
                                        ]
                                        }
                                    ],
                                    "temperature": 0,
                                    "response_format": { "type": "json_object" },
                                    "max_tokens": 2000,
                                    "top_p": 1,
                                    "frequency_penalty": 0,
                                    "presence_penalty": 0
                                    }),
                    ("https://api.openai.com/v1/chat/completions", {
                                    "model": "gpt-3.5-turbo-0125",
                                    "messages": [
                                        {
                                        "role": "system",
                                        "content": [
                                            {
                                            "text": "Objective: As a technical recruiter, you'\''re tasked with evaluating a candidate'\''s expertise in their technical domain based on their resume (‘resume_text’ and/or ‘linkedin_text’) and present/past employers'\'' descriptions (‘company_description’). Your goal is to identify the primary technical domain and up to three subdomains they have experience in, guided by their job responsibilities and the nature of their past employment.\n\nInstruction:\n\nContext Considerations: Pay close attention to the industry context, the technologies the candidate has worked with, and the scale and scope of their projects. \n\nDomain and Subdomain Guidelines: Refer to the provided list of domain categories to guide your analysis. Each main domain includes specific subdomains representing more detailed expertise. Stick to this list for your domain and subdomain selections.\n\nExclusion of Non-Technical Roles: Do not include roles that are not technically oriented or where the technical aspects are not clear. Focus solely on positions where the candidate'\''s technical skills and knowledge are directly applied.\n\nConsolidated Domain Categories:\n{ \"Domains\": { \"Data Analytics\": { \"Subdomains\": [ \"Visualization\", \"Statistical Analysis\", \"Data Cleaning and Wrangling\", \"Geospatial Analysis\", \"Time Series Analysis\", \"Sentiment Analysis\", \"Marketing Analytics\", \"Predictive Modeling\", \"ETL\" ] }, \"Data Scientist\": { \"Subdomains\": [ \"Hypothesis Testing\", \"Time Series Analysis\", \"Anomaly Detection\", \"Sentiment Analysis\", \"Causal Inference\", \"Bayesian Statistics\", \"Regression Analysis\", \"Principal Component Analysis (PCA)\", \"Recommendation Systems\", \"Fraud Detection\", \"Churn Prediction\", \"Customer Segmentation\", \"Simulations\", \"Price Optimization Models\", \"Cybersecurity\", \"Natural Language Processing\", \"Statistical Analysis\", \"Optimization\", \"Feature Engineering\", \"Automated Machine Learning\", \"Decision Trees\", \"Random Forests\", \"Neural Networks\" ] }, \"Machine Learning Engineer\": { \"Subdomains\": [ \"Deep Learning\", \"Computer Vision\", \"Natural Language Processing\", \"Reinforcement Learning\", \"Neural Networks\", \"Decision Trees\", \"Random Forests\", \"Optimization\", \"Autonomous Systems\", \"Algorithmic Trading\", \"Robot Control\", \"Automated Machine Learning\", \"Chatbot\", \"Quantum Computing\", \"Real-time ML\", \"Collaborative Filtering\", \"Signal Processing\", \"Cybersecurity\", \"Sensor Fusion\" ] }, \"MLOps Engineer\": { \"Subdomains\": [ \"ML-Ops\", \"Continuous Integration/ Deployment (CI/CD)\", \"Containerization\", \"Cloud Computing\", \"Distributed Computing\", \"DevOps Practices\", \"Data Lifecycle Management\", \"Cloud Security\", \"Deploying ML Models\" ] }, \"Machine Learning Researcher\": { \"Subdomains\": [ \"Deep Learning\", \"Natural Language Processing\", \"Computer Vision\", \"Reinforcement Learning\", \"Bayesian Statistics\", \"Semantic Segmentation\", \"Object Detection\", \"Image Recognition\", \"Natural Language Generation (NLG)\", \"Quantum Machine Learning\", ] }, \"Data Engineer, ML\": { \"Subdomains\": [ \"Data Pipelines\", \"Feature Engineering\", \"Data Cleaning and Wrangling\", \"ML-Ops\", \"Database Management\", \"Cloud Computing\", \"Distributed Computing\", \"Edge Computing\", \"Deploying ML Models\" \"Graph Databases\" ] }, \"Data Engineer, Big Data\": { \"Subdomains\": [ \"Big Data Analytics\", \"Distributed Computing\", \"Cloud Computing\", \"ETL\", \"Data Lifecycle Management\", \"Data Cleaning and Wrangling\", \"Database Management\", \"High-performance Computing (HPC)\", \"Data Governance\", \"Data Quality Management\" ] }, \"Data Engineer, software\": { \"Subdomains\": [ \"Software Development Practices\", \"Continuous Integration/Continuous Deployment (CI/CD)\", \"Database Management\", \"Data Security, Compliance, and Privacy\", \"Cloud Computing\", \"Microservices Architecture\", \"Data Lifecycle Management\", \"Network Architecture\", \"Data Governance\", \"Data Quality Management\" ] }, \"AI Engineer\": { \"Subdomains\": [ \"Machine Learning Models\", \"Deep Learning\", \"Natural Language Processing\", \"Computer Vision\", \"Model Optimization\", \"AI Ethics and Bias Mitigation\", \"Model Deployment\", \"Model Monitoring and Maintenance\", \"Reinforcement Learning\", \"Generative Models\" ] }, \"Generative AI Engineer\": { \"Subdomains\": [ \"Generative Adversarial Networks (GANs)\", \"Variational Autoencoders (VAEs)\", \"Transformer Models\", \"Text-to-Image Generation\", \"Voice Synthesis\", \"Content Creation AI\", \"Style Transfer\", \"DeepFakes Detection\", \"Music Generation\", \"Creative AI Applications\" ] }, \"Data Architect\": { \"Subdomains\": [ \"Data Modeling\", \"Data Warehouse Design\", \"Data Lake Architecture\", \"Metadata Management\", \"Data Governance\", \"Master Management\" }, \"DataOps Engineer\": { \"Subdomains\": [ \"Data Pipeline Automation\", \"Data Quality\", \"Data Governance\", \"Continuous Integration/Continuous Deployment for Data\", \"Monitoring and Logging for Data Systems\", \"Collaboration between Data Teams and Operations\", \"Data Security and Compliance\", \"Performance Optimization\", \"Data Storage and Computing Scalability\", \"Data Lifecycle Management\" ] }, \"AI Safety Engineer\": { \"Subdomains\": [ \"Risk Assessment\", \"Safety-critical AI Systems\", \"Incident Response for AI Systems\", \"AI Security\", \"Robustness and Reliability\", \"Transparency and Explainability\", \"Ethical Considerations\", \"AI Governance\", \"Safety by Design\", \"Monitoring and Evaluation\" ] }, \"Quantitative Analyst (Financial Industry)\": { \"Subdomains\": [ \"Quantitative Trading Strategies\", \"Risk Management\", \"Derivatives Pricing\", \"Financial Modeling\", \"Statistical Analysis\", \"Algorithmic Trading\", \"Portfolio Optimization\", \"Econometrics\", \"Machine Learning in Finance\", \"Market Microstructure Analysis\" ] }\n\nOutput Format: Document your findings using the following JSON structure for each position:\n{ \"domain_analysis\": \n[\n{\"job_title\": \"\", \n\"company_id\": \"\", \n\"identified_domain\": \"[Domain]\", \n\"subdomain\": [ \"[Subdomain 1]\", \"[Subdomain 2]\", \"[Subdomain 3]\" ] \n} // Repeat for each additional position \n]\n}\n",
                                            "type": "text"
                                            }
                                        ]
                                        },
                                        {
                                        "role": "user",
                                        "content": [
                                            {
                                            "type": "text",
                                            "text": resume_text +"\n" + companies_description
                                            }
                                        ]
                                        }
                                    ],
                                    "temperature": 0,
                                    "response_format": { "type": "json_object" },
                                    "max_tokens": 2000,
                                    "top_p": 1,
                                    "frequency_penalty": 0,
                                    "presence_penalty": 0
                                    }),
                    ("https://api.openai.com/v1/chat/completions", {
                                    "model": "gpt-3.5-turbo-0125",
                                    "messages": [
                                        {
                                        "role": "system",
                                        "content": [
                                            {
                                            "text": "Role: You are a technical recruiter.\n\nTask: Your task is to ANALYZE the resume_text and/or linkedin_text. For each education listed, you will:\n\ndetermine in which category this degree of candidate falls.\n\nThe categories are\n- None Degree Program\n- High School\n- Associate Degree\n- Bachelor's Degree\n- Master's Degree\n- Doctoral Degree\n\n\nOutput format: JSON\n\n{ \n\"educations\": [ \n{\n\"degree\": \"\",\n\"eduId\":\"\", \n\"field_of_study\": \"\", \n\"category\": \"\"\n}\n // Additional assessments for other positions go here \n] \n}",
                                            "type": "text"
                                            }
                                        ]
                                        },
                                        {
                                        "role": "user",
                                        "content": [
                                            {
                                            "type": "text",
                                            "text": education_info
                                            }
                                        ]
                                        }
                                    ],
                                    "temperature": 0,
                                    "response_format": { "type": "json_object" },
                                    "max_tokens": 2000,
                                    "top_p": 1,
                                    "frequency_penalty": 0,
                                    "presence_penalty": 0
                                    })
    ]
    return urls_and_data