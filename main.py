from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from pydantic import BaseModel
from src.exceptions import CustomExcetions
from openai import OpenAI
from src.prompt import model
from src.utils import response_formatter, check_overlap_all, matching_experience, map_talent_info
import os
import json
from src.pipeline.response_formatting import RawResponse
import sys
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class categorization(BaseModel):
    resume_text: str
    pdf: str = ''
    linkedin_text: str = ''
    companies_description: str = ''
    domain_categorization: bool = True
    job_function_extraction: bool = True
    industry_experience_extraction: bool = True
    # education: bool = True

app = FastAPI()

@app.post("/job_role")
async def job_role_function(categorizer: categorization):
    if categorizer.pdf != "":
        try:
            final_results = {}
            resume_text = categorizer.pdf
            companies_description = categorizer.companies_description
            response_obj = RawResponse(client=client, model=model[-1], resume=resume_text)
            pdf_text = response_obj.pdf_parser()

            with ThreadPoolExecutor() as executor:
                futures = []
                if categorizer.job_function_extraction:
                    futures.append(executor.submit(response_obj.job_function))
                if categorizer.domain_categorization:
                    futures.append(executor.submit(response_obj.domain_categorization, company_description=companies_description))
                if categorizer.industry_experience_extraction:
                    futures.append(executor.submit(response_obj.industry_experience, company_description=companies_description))

                for future in futures:
                    result = future.result()
                    if result:
                        final_results.update(result)


            final_dict = {"resume_information": final_results} 
            final = response_formatter(
                                        final_dict, job_functions = categorizer.job_function_extraction, 
                                        domain_categorization=categorizer.domain_categorization, 
                                        industry_experience= categorizer.industry_experience_extraction,
                                        )
            # print(final)
            # linkedin_text = json.loads(categorizer.linkedin_text)
            return map_talent_info(final_dict=final, linkenin_text=pdf_text)
        
        except Exception as e:
            raise CustomExcetions(e, sys)

            
    else:
        try:
            final_results = {}
            resume_text = categorizer.linkedin_text
            companies_description = categorizer.companies_description
            response_obj = RawResponse(client=client, model=model[2], resume=resume_text)

            with ThreadPoolExecutor() as executor:
                futures = []
                if categorizer.job_function_extraction:
                    futures.append(executor.submit(response_obj.job_function))
                if categorizer.domain_categorization:
                    futures.append(executor.submit(response_obj.domain_categorization, company_description=companies_description))
                if categorizer.industry_experience_extraction:
                    futures.append(executor.submit(response_obj.industry_experience, company_description=companies_description))

                for future in futures:
                    result = future.result()
                    if result:
                        final_results.update(result)


            final_dict = {"resume_information": final_results} 
            final = response_formatter(
                                        final_dict, job_functions = categorizer.job_function_extraction, 
                                        domain_categorization=categorizer.domain_categorization, 
                                        industry_experience= categorizer.industry_experience_extraction,
                                        )
            # print(final)
            linkedin_text = json.loads(categorizer.linkedin_text)

            if (len(final["profile_analysis"])-1) != len(json.loads(categorizer.linkedin_text)["data"]["experiences"]):
                with ThreadPoolExecutor() as executor:
                    futures = []
                    if categorizer.job_function_extraction:
                        futures.append(executor.submit(response_obj.job_function))
                    if categorizer.domain_categorization:
                        futures.append(executor.submit(response_obj.domain_categorization, company_description=companies_description))
                    if categorizer.industry_experience_extraction:
                        futures.append(executor.submit(response_obj.industry_experience, company_description=companies_description))

                    for future in futures:
                        result = future.result()
                        if result:
                            final_results.update(result)


                    final_dict = {"resume_information": final_results} 
            
                    final = response_formatter(
                                                final_dict, job_functions = categorizer.job_function_extraction, 
                                                domain_categorization=categorizer.domain_categorization, 
                                                industry_experience= categorizer.industry_experience_extraction,
                                                )

            # resume_information =  {
            #                         "experiences": map_talent_info(final_dict=final, linkenin_text=linkedin_text),
            #                         "overlapping_roles" : check_overlap_all(final["profile_analysis"]),
            #                         "mapping_info": matching_experience(request=json.loads(categorizer.linkedin_text), prompt_response=final)
            #                         }
            # return map_talent_info(final_dict=final, linkenin_text=linkedin_text)
            return final_dict
        
        except Exception as e:
            raise CustomExcetions(e, sys)

# from concurrent.futures import ThreadPoolExecutor
# from fastapi import FastAPI
# from pydantic import BaseModel
# from src.exceptions import CustomExcetions
# from openai import OpenAI
# from src.prompt import model
# from src.utils import response_formatter
# import os
# from src.pipeline.response_formatting import RawResponse
# import sys
# from dotenv import load_dotenv
import asyncio
import aiohttp

# load_dotenv()

# api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key)

# from concurrent.futures import ThreadPoolExecutor
# from fastapi import FastAPI
# from pydantic import BaseModel

async def fetch(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            res=  await response.json()
            return res["json"]
        
# app = FastAPI()

# class categorization(BaseModel):
#     resume_text: str
#     linkedin_text: str
#     companies_description: str = ''
#     domain_categorization: bool = True
#     job_function_extraction: bool = True
#     industry_experience_extraction: bool = True
#     education: bool = True



@app.post("/job_role_test")
async def job_role_function(categorizer: categorization):
    try:
        resume_text = categorizer.linkedin_text
        companies_description = categorizer.companies_description
        # response_obj = RawResponse(client=client, model=model[2], resume=resume_text)
        urls_and_data = [
        ("https://flowise-b8q7.onrender.com/api/v1/prediction/aff4dc52-6578-4a48-bec2-0e43e0654734", {"question":resume_text}),
        ("https://flowise-b8q7.onrender.com/api/v1/prediction/5e3f90b0-0e9a-4aad-9558-15a057a75fff", {"question": resume_text+"\n"+companies_description}),
        ("https://flowise-b8q7.onrender.com/api/v1/prediction/fe56b7e9-72cf-414d-ad64-f82a0d3509dc", {"question": resume_text})
        ]
        tasks = [fetch(url, data) for url, data in urls_and_data]
        results = await asyncio.gather(*tasks)
        # final_dict = final_results.update(results)
        
        # return resultsz
        final_dict = {"resume_information": (results)} 
        restructured_data = {"resume_information": {}}
        for section in final_dict["resume_information"]:
            for key, value in section.items():
                if key not in restructured_data["resume_information"]:
                    restructured_data["resume_information"][key] = []
                restructured_data["resume_information"][key].extend(value)
        # return final_dict

        final = response_formatter(
                            restructured_data, job_functions = categorizer.job_function_extraction, 
                            domain_categorization=categorizer.domain_categorization, 
                            industry_experience= categorizer.industry_experience_extraction,
                            )
        linkedin_text = json.loads(categorizer.linkedin_text)
        return map_talent_info(final_dict=final, linkenin_text=linkedin_text)
        # return final
    except Exception as e:
        raise CustomExcetions(e, sys)


