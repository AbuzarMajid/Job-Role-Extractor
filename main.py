from src.utils import chat_completion
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from pydantic import BaseModel
from src.exceptions import CustomExcetions
from openai import OpenAI
from src.prompt import JobRoleExtractor, model
import os
import sys
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
model_name = model[0]

class categorization(BaseModel):
    resume_text: str
    companies_description: str = ''


app = FastAPI()

@app.post("/job_role")
async def job_role_function(categorizer: categorization):
    try:
        resume_text = categorizer.resume_text
        companies_description = categorizer.companies_description
        content = resume_text + '\n\n' + companies_description
        with ThreadPoolExecutor() as executor:
            job_role_future = executor.submit(chat_completion, client = client, content = resume_text, model = model[0], prompt = JobRoleExtractor().job_role_extractor_instructions)
            job_role_categ_future = executor.submit(chat_completion, client=client, content=resume_text, model = model[0], prompt = JobRoleExtractor().role_categorization_instructions)
            domain_categ_future = executor.submit(chat_completion, client = client, content = content, model = model[1], prompt = JobRoleExtractor().domain_categorization)
            industry_eperience_future = executor.submit(chat_completion, client = client, content = content, model = model[0], prompt =  JobRoleExtractor().industry_experience)
        return {
                "job_role_function": job_role_future.result(),
                "role_categorization": job_role_categ_future.result(),
                "domain_categorization": domain_categ_future.result(),
                "industry_experience": industry_eperience_future.result()
                }
    
    except Exception as e:
        raise CustomExcetions(e, sys)
