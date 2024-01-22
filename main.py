from src.pipeline.pipeline import AssistantPipelines
from src.utils import domain_categ
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
        print(content)

        instructions_job_role = JobRoleExtractor().job_role_extractor_instructions
        instruction_job_role_categ = JobRoleExtractor().role_categorization_instructions
        with ThreadPoolExecutor() as executor:
            job_role_future = executor.submit(AssistantPipelines(client=client, model_name=model_name, content=resume_text, instructions=instructions_job_role).extraction)
            job_role_categ_future = executor.submit(AssistantPipelines(client=client, model_name=model_name, content=resume_text, instructions=instruction_job_role_categ).extraction)
            domain_categ_future = executor.submit(domain_categ, client = client, content = content)
        
        return {
                "job_role_function": job_role_future.result(),
                "role_categorization": job_role_categ_future.result(),
                "domain_categorization": domain_categ_future.result()
                }
    
    except Exception as e:
        raise CustomExcetions(e, sys)
