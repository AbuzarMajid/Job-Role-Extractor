from openai import OpenAI
from src.logger import logging
from src.exceptions import CustomExcetions
import sys
import json
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
                profile['job'] = job_function.get('job', None)
                profile['primary_function'] = job_function.get('primary_function', None).replace("N/A", "")
                profile['secondary_function'] = job_function.get('secondary_function', None).replace("N/A", "")
                profile['degree'] = job_function.get('degree', None).replace("N/A", "")
                profile['abbreviation'] = job_function.get('abbreviation', None).replace("N/A", "")
                profile['role_hierarchy'] = job_function.get('role_hierarchy', None)
                profile['employment_type'] = job_function.get('employment_type', None)
                profile['employment_sector'] = job_function.get('employment_sector', None)

                if industry_experience:    
                    industry_info = next((industry for industry in resume_information["resume_information"]['industry_analysis'] if industry["job"] == job_function["job"]), {"industry": ""})
                    profile['industry'] = industry_info.get('industry', "")    
            
                if domain_categorization:
                    domain_info = next((domain for domain in resume_information["resume_information"]['domain_analysis'] if domain["job"] == job_function["job"]), {"identified_domain": "", "subdomain": ""})
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
                profile['job'] = industry_experience_info.get('job', None)
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



# async def call_api(
#     url,
#     data,
#     api_key,
#     headers=None,
#     # text=False,
#     timeout=None,
# ):
#     headers = headers or {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {api_key}",
#     }

#     timeout = timeout or 60 * 1.5
#     client_timeout = aiohttp.ClientTimeout(
#         total=None, sock_connect=timeout, sock_read=timeout
#     )
#     async with aiohttp.ClientSession() as session:
#         session = session.post(url=url, json=data, headers=headers, timeout=client_timeout)
#         async with session as response:
#             response_text = ""
#             try:
#                 response_status_code = response.status
#                 response_text = await response.text()
#                 # if text:
#                 #     return response_text, response_status_code
#                 response_json = json.loads(response_text)
#                 return response_json, response_status_code
#             except:

#                 return response_text, response_status_code
