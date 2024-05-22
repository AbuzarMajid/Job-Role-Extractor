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
            return final, map_talent_info(final_dict=final, linkenin_text=linkedin_text)
        
        except Exception as e:
            raise CustomExcetions(e, sys)