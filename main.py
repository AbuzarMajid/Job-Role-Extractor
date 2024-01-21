from src.pipeline.pipeline import JobRoleFunctionExtractorPipeline
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
        jobe_role_obj = JobRoleFunctionExtractorPipeline(client=client, model_name=model_name, content=content, instructions=instructions_job_role)
        print("entry 1===============")
        job_role_function = await jobe_role_obj.extraction()
        content = categorizer.resume_text
        instruction_job_role_categ = JobRoleExtractor().role_categorization_instructions
        jobe_role__categ_obj = JobRoleFunctionExtractorPipeline(client=client, model_name=model_name, content=content, instructions=instruction_job_role_categ)
        print("entry 2=====================")
        categorized_role = await jobe_role__categ_obj.extraction()

        return {
                "job_role_function": job_role_function,
                "role_categorization": categorized_role,
                "instryctions": instruction_job_role_categ
                }
    
    except Exception as e:
        raise CustomExcetions(e, sys)
