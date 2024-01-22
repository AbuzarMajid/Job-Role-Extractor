import sys
from src.logger import logging
from src.utils import assistant_definition, create_messages, create_run, retrieve_run, show_messages, create_completion
from openai import OpenAI
import time
from src.exceptions import CustomExcetions

class AssistantPipelines():
    def __init__(self, client: OpenAI, model_name: str, content: str, instructions:str):
        self.client = client
        self.model_name = model_name
        self.content = content
        self.instructions = instructions

    def extraction(self):
        try:
            thread_id, assistant_id = assistant_definition(client=self.client, model_name=self.model_name, instructions=self.instructions)
            create_messages(client=self.client, thread_id=thread_id, content=self.content)
            run = create_run(client=self.client, thread_id=thread_id, assistant_id=assistant_id)
            status = True

            while status:

                retrieved_run = retrieve_run(client=self.client, thread_id=thread_id, run_id=run.id)
                logging.info(f'Status: {retrieved_run.status}')
                if retrieved_run.status in ['queued', 'in_progress']:
                    time.sleep(2)
                    continue

                elif retrieved_run.status == 'requires_action':
                    return "Exception Occurs: invalid funciton running"
                    

                elif retrieved_run.status == 'completed':
                    show_message = show_messages(client=self.client, thread_id=thread_id)
                    logging.info('Successfully shown message')
                    status = False
                    return show_message

                elif retrieved_run.status in ['cancelling', 'cancelled', 'failed', 'expired']:
                    user_message = f'Run Status: {retrieved_run.status}'
                    logging.info(user_message)
                    status =False
                    return user_message
                
        except Exception as e:
            raise CustomExcetions(e, sys)

