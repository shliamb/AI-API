import logging
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)
from typing import List, Optional, Union




class AssistOpenAI:

    '''

    Основные методы взаимодействия с Ассистентом, каналами, запусками и другими сущностями.  
    Объект клиента (client – клиент) OpenAI создаётся и используется непосредственно в месте 
    инициализации (launch point – точка запуска).

    '''

    def __init__(self, client_openai):
        self.client = client_openai



    # Assistent:
    async def create_assist(self, name: str, instructions: str, model: str, tools: List) -> Optional[str]:
        '''Добавление нового Ассистента'''
        try:
            response = await self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                model=model,
                tools=tools
            )
            return getattr(response, 'id', None)
        
        except Exception as e:
            logging.error(f"Failed to create assistant: {e}")
            return None
    

    async def list_assist(self, limit: int = 20) -> Optional[List]:
        '''Получение списка ассистентов (по умолчанию 20)'''
        try:
            response = await self.client.beta.assistants.list(
                order="desc",
                limit=limit
            )
            return getattr(response, 'data', None)

        except Exception as e:
            logging.error(f"list_assist failed: {e}")
            return None




    async def get_assist(self, assistant_id: str):
        '''Получение данных Ассистента'''
        try:
            response = await self.client.beta.assistants.retrieve(assistant_id)
            return response or None

        except Exception as e:
            logging.error(f"get_assist failed: {e}")
            return None
    


    async def delete_assist(self, assistant_id: str) -> dict:
        '''Удаление Ассистента'''
        try:
            response = await self.client.beta.assistants.delete(assistant_id)
            return response or None

        except Exception as e:
            logging.error(f"delete_assist failed: {e}")
            return None
    

    # Threads:
    async def create_tread(self) -> dict:
        '''Добавление пустого канала'''
        try:
            empty_thread = await self.client.beta.threads.create()
            return getattr(empty_thread, 'id', None)
        
        except Exception as e:
            logging.error(f"create_tread failed: {e}")
            return None


    async def create_tread_and_message(self, message: str) -> str:
        '''Добавление канала + добавление сообщения'''
        try:
            message_thread = await self.client.beta.threads.create(
                messages=[
                    {
                    "role": "user",
                    "content": message
                    }
                ]
            )
            return getattr(message_thread, 'id', None)
        
        except Exception as e:
            logging.error(f"create_tread_and_message failed: {e}")
            return None
    

    async def get_tread(self, thread_id: str) -> dict:
        '''Получение данных канала'''
        try:
            my_thread = await self.client.beta.threads.retrieve(thread_id)
            return my_thread or None
        
        except Exception as e:
            logging.error(f"get_tread failed: {e}")
            return None
    

    async def delete_tread(self, thread_id: str) -> str:
        '''Удаление канала'''
        try:
            response = await self.client.beta.threads.delete(thread_id)
            return response or None

        except Exception as e:
            logging.error(f"Failed to delete_tread: {e}")
            return None


    # Create Message:
    async def create_message(self, thread_id: str, message: str) -> dict:
        '''Добавление сообщения в канал'''
        try:
            thread_message = await self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message
            )
            return thread_message or None
        
        except Exception as e:
            logging.error(f"Failed to create_message: {e}")
            return None
    


    async def list_message(self, thread_id: str) -> List:
        '''Список сообщений канала'''
        try:
            thread_messages = await self.client.beta.threads.messages.list(thread_id)
            return getattr(thread_messages, 'data', None)

        except Exception as e:
            logging.error(f"Failed to list_message: {e}")
            return None


    # Run Assistent:
    async def run_assist(self, assist_id: str, thread_id: str) -> str:
        '''Запуск Ассистента'''
        try:
            run = await self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assist_id
            )
            return getattr(run, 'id', None)
        
        except Exception as e:
            logging.error(f"Failed to run_assist: {e}")
            return None
    


    async def create_tread_and_run_assist(self, assist_id: str, message: str) -> str:
        '''Создание канала и запуск Ассистента в один запрос'''
        try:
            run = await self.client.beta.threads.create_and_run(
                assistant_id=assist_id,
                thread={
                    "messages": [
                    {"role": "user", "content": message}
                    ]
                }
            )
            return getattr(run, 'id', None)

        except Exception as e:
            logging.error(f"Failed to create_tread_and_run_assist: {e}")
            return None
    


    async def cansel_run(self, run_id: str, thread_id: str):
        '''Отменяет выполнение которое находится в процессе'''
        try:
            run = await self.client.beta.threads.runs.cancel(
                thread_id=thread_id,
                run_id=run_id
            )
            return run or None
        
        except Exception as e:
            logging.error(f"Failed to cansel_run: {e}")
            return None

    


    # Get Respounce:
    async def get_runs_threads(self, run_id: str, thread_id: str) -> tuple:
        '''Получение ответа'''
        try:
            run_status = await self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )

            if not run_status:
                return None, None
            
            status = run_status.status
            tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
            return status, tool_calls
        
        except Exception as e:
            logging.error(f"Failed to Respounce get_runs_threads: {e}")
            return None, None