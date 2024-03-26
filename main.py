from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from pydantic import BaseModel
from src.exceptions import CustomExcetions
from openai import OpenAI
from src.prompt import model
from src.utils import response_formatter
import os
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
    companies_description: str = ''
    domain_categorization: bool = True
    job_function_extraction: bool = True
    industry_experience_extraction: bool = True

app = FastAPI()

@app.post("/job_role")
async def job_role_function(categorizer: categorization):
    try:
        final_results = {}
        resume_text = categorizer.resume_text
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

        resume_information =  {"resume_information": response_formatter(final_dict, job_functions = categorizer.job_function_extraction, 
                                                                        domain_categorization=categorizer.domain_categorization, 
                                                                        industry_experience= categorizer.industry_experience_extraction)}
        return resume_information
    
    except Exception as e:
        raise CustomExcetions(e, sys)