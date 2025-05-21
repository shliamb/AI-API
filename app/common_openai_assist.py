import logging
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)
from typing import List, Union




class AssistOpenAI:

    '''

    Основные методы взаимодействия с Ассистентом, каналами, запусками и другими сущностями.  
    Объект клиента (client – клиент) OpenAI создаётся и используется непосредственно в месте 
    инициализации (launch point – точка запуска).

    '''

    def __init__(self, client_openai):
        self.client = client_openai


    # Assistent:
    async def create_assist(self, name: str, instructions: str, model: str, tools: List) -> Union[str, None]:
        '''Добавление нового Ассистента'''
        try:
            assistant = await self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                model=model,
                tools=tools
            )
            return assistant.id
        
        except Exception as e:
            logging.error(f"Failed to create assistant: {e}")
            return None
    
    async def list_assist(self, limit: int = 20) -> List:
        '''Получение списка ассистентов (default 20)'''
        my_assistants = await self.client.beta.assistants.list(
            order="desc",
            limit=limit
        )
        return my_assistants.data

    async def get_assist(self, assistant_id: str) -> dict:
        '''Получение данных Ассистента'''
        my_assistant = await self.client.beta.assistants.retrieve(assistant_id)
        return my_assistant
    
    async def delete_assist(self, assistant_id: str) -> dict:
        '''Удаление Ассистента'''
        response = await self.client.beta.assistants.delete(assistant_id)
        return response
    

    # Threads:
    async def create_tread(self) -> dict:
        '''Добавление пустого канала'''
        empty_thread = await self.client.beta.threads.create()
        return empty_thread.id

    async def create_tread_and_message(self, message: str) -> str:
        '''Добавление канала + добавление сообщения'''
        message_thread = await self.client.beta.threads.create(
            messages=[
                {
                "role": "user",
                "content": message
                }
            ]
        )
        return message_thread.id
    
    async def get_tread(self, thread_id: str) -> dict:
        '''Получение данных канала'''
        my_thread = await self.client.beta.threads.retrieve(thread_id)
        return my_thread
    
    async def delete_tread(self, thread_id: str) -> dict:
        '''Удаление канала'''
        response = await self.client.beta.threads.delete(thread_id)
        return response
    

    # Create Message:
    async def create_message(self, thread_id: str, message: str) -> dict:
        '''Добавление сообщения в канал'''
        thread_message = await self.client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
        )
        return thread_message
    
    async def list_message(self, thread_id: str) -> List:
        '''Список сообщений канала'''
        thread_messages = await self.client.beta.threads.messages.list(thread_id)
        return thread_messages.data
    

    # Run Assistent:
    async def run_assist(self, assist_id: str, thread_id: str) -> str:
        '''Запуск Ассистента'''
        run = await self.client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assist_id
        )
        return run.id
    
    async def create_tread_and_run_assist(self, assist_id: str, message: str) -> str:
        '''Создание канала и запуск Ассистента в один запрос'''
        run = await self.client.beta.threads.create_and_run(
            assistant_id=assist_id,
            thread={
                "messages": [
                {"role": "user", "content": message}
                ]
            }
        )
        return run.id
    
    async def cansel_run(self, run_id: str, thread_id: str):
        '''Отменяет выполнение которое находится в процессе'''
        run = await self.client.beta.threads.runs.cancel(
        thread_id=thread_id,
        run_id=run_id
        )
        return run
    
    # Get Respounce:
    async def get_runs_threads(self, run_id: str, thread_id: str) -> tuple:
        '''Получение ответа'''
        try:
            run_status = await self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )
            
            if not run_status:
                return None
            
            status = run_status.status
            tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
            return status, tool_calls
        
        except Exception as e:
            logging.error(f"Failed to Respounce get_runs_threads: {e}")
            return None