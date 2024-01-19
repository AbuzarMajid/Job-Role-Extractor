from src.pipeline.pipeline import JobRoleFunctionExtractorPipeline
from fastapi import FastAPI
from pydantic import BaseModel
from src.exceptions import CustomExcetions
from openai import OpenAI
import os
import sys
from src.prompt import model
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
model_name = model[1]
class Jobfunction(BaseModel):
    resume_text: str
    company_descriptions: str
    positions: str

app = FastAPI()

@app.post("/")
async def job_role_function(jobfunction: Jobfunction) -> dict:
    try:
        content = jobfunction.resume_text +'\n\n' + jobfunction.company_descriptions + '\n\n' + jobfunction.positions
        pipeline = JobRoleFunctionExtractorPipeline(client=client, model_name=model_name, content=content)
        job_role_function = pipeline.extraction()
        return {"job_role_function": job_role_function}
    
    except Exception as e:
        raise CustomExcetions(e, sys)
