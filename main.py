from src.pipeline.pipeline import JobRoleFunctionExtractorPipeline
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from pydantic import BaseModel
from src.exceptions import CustomExcetions
from openai import OpenAI
from src.prompt import JobRoleExtractor
import os
import sys
from src.prompt import model
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
model_name = model[0]

class categorization(BaseModel):
    resume_text: str

app = FastAPI()

@app.post("/job_role")
async def job_role_function(categorizer: categorization):
    try:
        content = categorizer.resume_text
        instructions_job_role = JobRoleExtractor().job_role_extractor_instructions
        instruction_job_role_categ = JobRoleExtractor().role_categorization_instructions
        with ThreadPoolExecutor() as executor:
            job_role_future = executor.submit(
                JobRoleFunctionExtractorPipeline(client=client, model_name=model_name, content=content, instructions=instructions_job_role).extraction)
            job_role_categ_future = executor.submit(JobRoleFunctionExtractorPipeline(client=client, model_name=model_name, content=content, instructions=instruction_job_role_categ).extraction)
        
        return {
                "job_role_function": job_role_future.result(),
                "role_categorization": job_role_categ_future.result(),
                "instrcctions": instructions_job_role
                }
    
    except Exception as e:
        raise CustomExcetions(e, sys)
