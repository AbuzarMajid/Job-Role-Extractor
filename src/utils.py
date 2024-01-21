from openai import OpenAI
from src.logger import logging
from src.exceptions import CustomExcetions
import sys
from src.prompt import JobRoleExtractor

    
def create_run(client: OpenAI, thread_id, assistant_id):
        try:
            run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id)
            logging.info('Successfully Created Run')
            return run
        except Exception as e:
            raise CustomExcetions(e, sys)
        

def assistant_definition(client: OpenAI, model_name, instructions):
    try:
        # defining assisatnt for the category in which the job description is given
        assistant = client.beta.assistants.create(
            instructions=instructions,
            name="Job Role Extractor",
            model=model_name
        )
        assistant_id = assistant.id
        logging.info('Assistant defined')
        #defining a thread for that assistant
        thread = client.beta.threads.create()
        thread_id = thread.id
        logging.info('Thread defined')
        return thread_id, assistant_id
    
    except Exception as e:
        raise CustomExcetions(e, sys)


def retrieve_run(client: OpenAI, thread_id, run_id):
    try:
        run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id)
        logging.info("successfully retrieved run")
        return run
    except Exception as e:
        raise CustomExcetions(e, sys)
    
def create_messages(client:OpenAI, thread_id, content):
    try:
        message = client.beta.threads.messages.create(
        thread_id= thread_id,
        role="user",
        content=content
        )
        logging.info("successfully defined message")
        return message

    except Exception as e:
        raise e
    
def show_messages(client: OpenAI, thread_id):
    try:
        messages = client.beta.threads.messages.list(
        thread_id= thread_id)
        response = messages.data[0].content[0].text.value
        logging.info('Successfully retrieved message')
        return response
    except Exception as e:
        raise CustomExcetions(e, sys)