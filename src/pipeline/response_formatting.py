import sys
from src.logger import logging
from src.exceptions import CustomExcetions
from openai import OpenAI
import requests

class RawResponse:
    def __init__(self, client: OpenAI, model, resume):
        self.client = client
        self.model = model
        self.resume = resume
        
    def job_function(self):
        try:
            logging.info("entered job function")
            req_body = {
                "question": self.resume,
                "overrideConfig": {
                    "modelName": self.model,
                }
            }
            response = requests.post(url="https://flowise-b8q7.onrender.com/api/v1/prediction/aff4dc52-6578-4a48-bec2-0e43e0654734", json=req_body)
            return response.json()["json"]
            
        except Exception as e:
            raise CustomExcetions(e, sys)
        
    def domain_categorization(self, company_description):
        try:
            # prompt_obj = JobRoleExtractor()
            logging.info("entered domain")
            content = self.resume + "\n" + company_description
            req_body = {
                "question": content,
                "overrideConfig": {
                "modelName": self.model,
                }
            }
            response = requests.post(url="https://flowise-b8q7.onrender.com/api/v1/prediction/fe56b7e9-72cf-414d-ad64-f82a0d3509dc", json=req_body)
            return response.json()["json"]
            
        except Exception as e:
            raise CustomExcetions(e, sys)
        
    def industry_experience(self, company_description):
        try:
            # prompt_obj = JobRoleExtractor()
            logging.info("entered industry")
            content = self.resume + "\n" + company_description
            req_body = {
                "question": content,
                "overrideConfig": {
                "modelName": self.model,
                }
            }
            response = requests.post(url="https://flowise-b8q7.onrender.com/api/v1/prediction/5e3f90b0-0e9a-4aad-9558-15a057a75fff", json=req_body)
            return response.json()["json"]

        except Exception as e:
            raise CustomExcetions(e, sys)
        
    def education(self):
        try:
            # prompt_obj = JobRoleExtractor()
            logging.info("entered education")
            req_body = {
                "question": self.resume,
                "overrideConfig": {
                "modelName": self.model,
                }
            }
            response = requests.post(url="https://flowise-b8q7.onrender.com/api/v1/prediction/323c48d5-058b-401a-8a6d-8188e3bb5568", json=req_body)
            return response.json()["json"]

        except Exception as e:
            raise CustomExcetions(e, sys)
        
    def pdf_parser(self):
        try:
            # prompt_obj = JobRoleExtractor()
            logging.info("entered pdf parser")
            req_body = {
                "question": self.resume,
                "overrideConfig": {
                "modelName": self.model,
                }
            }
            response = requests.post(url="https://flowise-b8q7.onrender.com/api/v1/prediction/a3f7cd53-7081-436a-b394-9c83a39fe491", json=req_body)
            return response.json()["json"]

        except Exception as e:
            raise CustomExcetions(e, sys)
        
