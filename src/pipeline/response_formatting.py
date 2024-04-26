import os
import sys
from src.logger import logging
from src.exceptions import CustomExcetions
from src.utils import create_chat_completion
from src.prompt import JobRoleExtractor
from openai import OpenAI

class RawResponse:
    def __init__(self, client: OpenAI, model, resume):
        self.client = client
        self.model = model
        self.resume = resume
        
    def job_function(self, prompt):
        try:
            # prompt_obj = JobRoleExtractor()
            message = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": self.resume}
            ]
            response = create_chat_completion(client=self.client, model_name=self.model, messages=message)
            return response
            
        except Exception as e:
            raise CustomExcetions(e, sys)
        
    def domain_categorization(self, prompt, company_description):
        try:
            # prompt_obj = JobRoleExtractor()
            content = self.resume + "\n" + company_description
            message = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ]
            response = create_chat_completion(client=self.client, model_name=self.model, messages=message)
            return response
            
        except Exception as e:
            raise CustomExcetions(e, sys)
        
    def industry_experience(self, prompt, company_description):
        try:
            # prompt_obj = JobRoleExtractor()
            content = self.resume + "\n" + company_description
            message = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ]
            response = create_chat_completion(client=self.client, model_name=self.model, messages=message)
            return response
            
        except Exception as e:
            raise CustomExcetions(e, sys)
        
