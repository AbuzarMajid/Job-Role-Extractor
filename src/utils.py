from openai import OpenAI
from src.logger import logging
from src.exceptions import CustomExcetions
import sys
import json
from datetime import datetime
# import aiohttp

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


def response_formatter(resume_information: dict, job_functions: bool, domain_categorization: bool, industry_experience: bool):
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
            
            # if education:
            #     if resume_information["resume_information"]['education']:
            #         education = resume_information["resume_information"]['education']
            #         profile_analysis.append(education)

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

            # if education:
            #     if resume_information["resume_information"]['education']:
            #         education = resume_information["resume_information"]['education']
            #         profile_analysis.append(education)

            return {"profile_analysis": profile_analysis}
        
        # # when domain categroizatrion is true only
        # elif domain_categorization and education:
        #     return {"Domain Categorizaton": resume_information["resume_information"]["domain_analysis"], "education": resume_information["resume_information"]["education"]}

        # elif industry_experience and education:
        #     return {"Industry Experience": resume_information["resume_information"]["industry_analysis"], "education": resume_information["resume_information"]["education"]}

        elif domain_categorization:
            return {"Domain Categorizaton": resume_information["resume_information"]["domain_analysis"]}
        
        # when industry expeirience is try only
        elif industry_experience:
            return {"Industry Experience": resume_information["resume_information"]["industry_analysis"]}
        
        # elif education:
        #     return {"Industry Experience": resume_information["resume_information"]["education"]}

        if not (job_functions or domain_categorization or industry_experience):
            return{"message": "At least one of the options (job_functions, domain_categorization, industry_experience) must be True."}
        
    except Exception as e:
        raise CustomExcetions(e, sys)
    
from datetime import datetime

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

def map_talent_info(final_dict, linkenin_text):
    merge_dicts = lambda x, y: {**x, **y}
    mapped_data = []
    # mapped_data = [
    #     merge_dicts(company_data, next((profile for profile in final_dict["profile_analysis"] if profile.get("job_title") == company_data["title"]), {}))
    #     for company_data in linkenin_text["data"]["experiences"]
    # ]
    mapped_data = [
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
    for each in mapped_data:
        each.pop("job_title", None)

    linkenin_text["data"]["experiences"] = mapped_data
    industries = final_dict["profile_analysis"][-1]["overal_industry"]
    score = final_dict["profile_analysis"][-1]["score"]
    industry_scores = {}

    # Map the experience lists together
    for i in range(len(industries)):
        industry_scores[industries[i]] = score[i]

    # Deleting the title key from final dictionery


    linkenin_text["overlapping_roles"] = check_overlap_all(final_dict["profile_analysis"])
    linkenin_text["mapping_info"] = matching_experience(request=linkenin_text, prompt_response=final_dict)

    linkenin_text["overall_experience"] = industry_scores
    return (linkenin_text)