from fastapi import FastAPI
from pydantic import BaseModel
from src.exceptions import CustomExcetions
from openai import OpenAI
from src.prompt import model
from src.utils import response_formatter, map_talent_info, call_api, get_urls_and_headers, map_talent_info_pdf, response_formatter_pdf
import os
import json
from src.pipeline.response_formatting import RawResponse
import sys
from dotenv import load_dotenv
import asyncio

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from pydantic import BaseModel

class categorization(BaseModel):
    resume_text: str
    pdf: str = ''
    linkedin_text: str = ''
    companies_description: str = ''
    domain_categorization: bool = True
    job_function_extraction: bool = True
    industry_experience_extraction: bool = True
    education: bool = True

app = FastAPI()



@app.post("/job_role_test")
async def job_role_function(categorizer: categorization):
    if categorizer.pdf != "":
        try:
            resume_text = categorizer.pdf
            companies_description = categorizer.companies_description
            response_obj = RawResponse(client=client, model=model[-1], resume=resume_text)
            pdf_text = response_obj.pdf_parser()
            urls_and_headers = get_urls_and_headers(
                resume_text=resume_text, 
                companies_description=companies_description, 
                education_info=f"""{pdf_text["data"]["educations"]}"""
            )
            # print(pdf_text["data"]["educations"])
            tasks = [
            call_api(url, data, api_key=api_key) 
            for url, data in urls_and_headers
        ]        
            results = await asyncio.gather(*tasks)

            final_dict = {"resume_information": results} 
            restructured_data = {"resume_information": {}}
            for section in final_dict["resume_information"]:
                print(section)
                for key, value in section.items():
                    if key not in restructured_data["resume_information"]:
                        restructured_data["resume_information"][key] = []
                    restructured_data["resume_information"][key].extend(value)
            # return final_dict

            final = response_formatter_pdf(
                                        restructured_data, job_functions = categorizer.job_function_extraction, 
                                        domain_categorization=categorizer.domain_categorization, 
                                        industry_experience= categorizer.industry_experience_extraction,
                                        )
            response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                "role": "system",
                "content": [
                    {
                    "text": "Role: You are a technical recruiter. Analyze the candidate's resume_text and/or linkedin_text, considering each position they held, the job title in the context of the company they work at, the job responsibilities for each position, relevant keywords and phrases that indicate the position's experience level and responsibilities, as well as the overall years of experience. \n\nUse the following criteria to categorize candidates into one of the listed categories:\n\n1. Entry Level: Candidates with minimal experience or recent graduates.\n2. Mid Level: Individual contributors with moderate experience and some specialized skills.\n3. Senior: Individual contributors with extensive experience and advanced skills, often handling significant responsibilities.\n4. Team Lead: Candidates who guide or influence others without direct reports, requiring leadership and specialized expertise, often including both individual contributions and partial leadership responsibilities.\n5. Manager: Candidates with direct management responsibilities, typically overseeing fewer than 5 direct reports, and involved in strategic decision-making and leadership.\n6. Director: Senior management candidates with clear titles indicating they manage larger teams, typically overseeing 5 or more people, with significant strategic and operational responsibilities. \n\nFor each resume or profile:- \nAssess the candidate's experience and responsibilities.- Match the candidate's profile to the appropriate category based on the descriptions provided. JSON Output: \"seniority_level\": \"[level: Entry Level, Mid-Level, Senior, Team Lead, Manager, Director\"],\n\nOutput Format: JSON\n{\n\"seniority_level\": \"\"\n}",
                    "type": "text"
                    },
                    {
                    "text": resume_text,
                    "type": "text"
                    }
                ]
                }
            ],
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
            talent_info = map_talent_info(final_dict=final, linkenin_text=linkedin_json)
            talent_info["data"]["seniority_level"] = json.loads(response.choices[0].message.content)["seniority_level"]
            # linkedin_text = json.loads(categorizer.linkedin_text)
            return map_talent_info(final_dict=final, linkenin_text=linkedin_json)
        
        except Exception as e:
            raise CustomExcetions(e, sys)
    else:
        try:
            resume_text = categorizer.linkedin_text
            companies_description = categorizer.companies_description
            linkedin_json = json.loads(categorizer.linkedin_text)
            urls_and_headers = get_urls_and_headers(
                resume_text=resume_text, 
                companies_description=companies_description, 
                education_info=f"""{linkedin_json["data"]["educations"]}"""
            )
            tasks = [
            call_api(url, data, api_key=api_key) 
            for url, data in urls_and_headers
        ]        
            results = await asyncio.gather(*tasks)
            
            # return resultsz
            final_dict = {"resume_information": results} 
            restructured_data = {"resume_information": {}}
            for section in final_dict["resume_information"]:
                    for key, value in section.items():
                        if key not in restructured_data["resume_information"]:
                            restructured_data["resume_information"][key] = []
                        restructured_data["resume_information"][key].extend(value)

            final = response_formatter(
                                restructured_data, job_functions = categorizer.job_function_extraction, 
                                domain_categorization=categorizer.domain_categorization, 
                                industry_experience= categorizer.industry_experience_extraction,
                                education=categorizer.education
                                )
            
            response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                "role": "system",
                "content": [
                    {
                    "text": "Role: You are a technical recruiter. Analyze the candidate's resume_text and/or linkedin_text, considering each position they held, the job title in the context of the company they work at, the job responsibilities for each position, relevant keywords and phrases that indicate the position's experience level and responsibilities, as well as the overall years of experience. \n\nUse the following criteria to categorize candidates into one of the listed categories:\n\n1. Entry Level: Candidates with minimal experience or recent graduates.\n2. Mid Level: Individual contributors with moderate experience and some specialized skills.\n3. Senior: Individual contributors with extensive experience and advanced skills, often handling significant responsibilities.\n4. Team Lead: Candidates who guide or influence others without direct reports, requiring leadership and specialized expertise, often including both individual contributions and partial leadership responsibilities.\n5. Manager: Candidates with direct management responsibilities, typically overseeing fewer than 5 direct reports, and involved in strategic decision-making and leadership.\n6. Director: Senior management candidates with clear titles indicating they manage larger teams, typically overseeing 5 or more people, with significant strategic and operational responsibilities. \n\nFor each resume or profile:- \nAssess the candidate's experience and responsibilities.- Match the candidate's profile to the appropriate category based on the descriptions provided. JSON Output: \"seniority_level\": \"[level: Entry Level, Mid-Level, Senior, Team Lead, Manager, Director\"],\n\nOutput Format: JSON\n{\n\"seniority_level\": \"\"\n}",
                    "type": "text"
                    },
                    {
                    "text": resume_text,
                    "type": "text"
                    }
                ]
                }
            ],
            temperature=0,
            max_tokens=256,
            response_format={"type": "json_object"},
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
            talent_info = map_talent_info(final_dict=final, linkenin_text=linkedin_json)
            talent_info["data"]["seniority_level"] = json.loads(response.choices[0].message.content)["seniority_level"]
            # linkedin_text = json.loads(categorizer.linkedin_text)
            return map_talent_info(final_dict=final, linkenin_text=linkedin_json)
        
            # return results
        except Exception as e:  
            raise CustomExcetions(e, sys)