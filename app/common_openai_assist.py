from setup_config_logger import setup_logger
logger_ai = setup_logger('ai', '/log/ai.log')
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
            logger_ai.error(f"Failed to create assistant: {e}")
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
            logger_ai.error(f"list_assist failed: {e}")
            return None




    async def get_assist(self, assistant_id: str):
        '''Получение данных Ассистента'''
        try:
            response = await self.client.beta.assistants.retrieve(assistant_id)
            return response or None

        except Exception as e:
            logger_ai.error(f"get_assist failed: {e}")
            return None
    


    async def delete_assist(self, assistant_id: str) -> dict:
        '''Удаление Ассистента'''
        try:
            response = await self.client.beta.assistants.delete(assistant_id)
            return response or None

        except Exception as e:
            logger_ai.error(f"delete_assist failed: {e}")
            return None
    

    # Threads:
    async def create_tread(self) -> dict:
        '''Добавление пустого канала'''
        try:
            empty_thread = await self.client.beta.threads.create()
            return getattr(empty_thread, 'id', None)
        
        except Exception as e:
            logger_ai.error(f"create_tread failed: {e}")
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
            logger_ai.error(f"create_tread_and_message failed: {e}")
            return None
    

    async def get_tread(self, thread_id: str) -> dict:
        '''Получение данных канала'''
        try:
            my_thread = await self.client.beta.threads.retrieve(thread_id)
            return my_thread or None
        
        except Exception as e:
            logger_ai.error(f"get_tread failed: {e}")
            return None
    

    async def delete_tread(self, thread_id: str) -> str:
        '''Удаление канала'''
        try:
            response = await self.client.beta.threads.delete(thread_id)
            return response or None

        except Exception as e:
            logger_ai.error(f"Failed to delete_tread: {e}")
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
            logger_ai.error(f"Failed to create_message: {e}")
            return None
    


    async def list_message(self, thread_id: str) -> List:
        '''Список сообщений канала'''
        try:
            thread_messages = await self.client.beta.threads.messages.list(thread_id)
            return getattr(thread_messages, 'data', None)

        except Exception as e:
            logger_ai.error(f"Failed to list_message: {e}")
            return None


    # Run Assistent:
    async def run_assist(self, assist_id: str, thread_id: str) -> str:
        '''Запуск Ассистента'''
        try:
            run = await self.client.beta.threads.runs.create(
                thread_id=thread_id,
                tool_choice="auto",
                assistant_id=assist_id
            )
            return getattr(run, 'id', None)
        
        except Exception as e:
            logger_ai.error(f"Failed to run_assist: {e}")
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
            logger_ai.error(f"Failed to create_tread_and_run_assist: {e}")
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
            logger_ai.error(f"Failed to cansel_run: {e}")
            return None

    


    # Get Respounce:
    async def get_runs_threads(self, run_id: str, thread_id: str) -> dict:
        '''Retrieves (получает) response from thread run'''
        try:
            run_status = await self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )

            status = run_status.status

            if status == "completed":
                messages = await self.client.beta.threads.messages.list(
                    thread_id=thread_id
                )
                
                assistant_messages = [] # assistant_messages = [msg for msg in messages.data if msg.role == "assistant"]
                for msg in messages.data:
                    if msg.role == "assistant":
                        assistant_messages.append(msg)
                
                if assistant_messages:
                    try:
                        content = assistant_messages[0].content
                        last_assist_message = content[0].text.value if content and hasattr(content[0], 'text') else "empty content"
                        return {"status": status, "message": last_assist_message, "response": run_status}
                    
                    except (IndexError, AttributeError):
                        logger_ai.warning(f"Could not extract message content: {e}")
                        return {"status": status, "message": None, "response": run_status}

                return {"status": status, "message": None, "response": run_status}
                
            if status == "requires_action":
                required_action = getattr(run_status, "required_action", None)
                tool_outputs = getattr(required_action, "submit_tool_outputs", None) if required_action else None
                tool_calls = getattr(tool_outputs, "tool_calls", None) if tool_outputs else None                
                return {"status": status, "tool_calls": tool_calls or None,"response": run_status} # "tool_outputs": tool_outputs or None,

            return {"status": status, "response": run_status}

        except Exception as e:
            logger_ai.error(f"Failed to get_runs_threads: {e}")
            return {"error": str(e), "response": None}
        

    # Returning Result Assist:
    async def returning_result_assist(self, run_id: str, thread_id: str, tool_outputs: List):
        '''
        Возвращает результат Ассистенту
        tool_outputs - список сформированных при работе функций результатов

        Пример tool_outputs:
        tool_outputs=[
            {
                "tool_call_id": "435353",
                "output": "15"
            },
            {
                "tool_call_id": "3565464",
                "output": None
            }
        ]
        '''

        try:
            output = await self.client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run_id,
                tool_outputs=tool_outputs
            )
            return output or None
        
        except Exception as e:
            logger_ai.error(f"Failed to oa_returning_result_assist: {e}")
            return {"error": str(e), "response": None}



# [None, [{'id': 'call_8jH3IuhNut9cSGU2lPmwEb7L', 'function': {'arguments': '{"a":34,"b":56}', 'name': 'add'}, 'type': 'function'}]]
# ['Да, верно. Вы можете задать пример задачи, и я помогу вам её решить. Например, вы можете попросить сложить или умножить два числа, или задать любой другой вопрос, который вас интересует. Дайте знать, чем я могу вам помочь!', 'ok']
