# Base
import logging
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)
from openai import AsyncOpenAI, RateLimitError, OpenAIError
# import asyncio
import json
# Service
from keys import API_KEY_OPENAI
# from config import DEF_MOD_OPENAI
from common_openai_assist import AssistOpenAI

client = AsyncOpenAI(api_key=API_KEY_OPENAI)
assist = AssistOpenAI(client)




# Запуск асистента кастомно:
async def oa_asist_custom_0525(data:dict) -> dict:

    '''
    Если указаны assistant_id и thread_id — используется существующий ассистент и поток.  
    Если одного из параметров нет — недостающее создаётся автоматически.  

    Если передан user_content, сообщение отправляется в поток, и запускается выполнение ассистента (run).  
    Если user_content отсутствует — выполнение не инициируется, возвращаются только assistant_id и thread_id.  

    Ответ в любом случае содержит:  
    - assistant_id  
    - thread_id  
    - run_id (только если был запущен run)
    
    '''

    name = data.get("name")
    instructions = data.get("instructions")
    model = data.get("model")
    user_content = data.get("user_content")
    str_tools = data.get("tools") 
    tools = json.loads(str_tools) if str_tools else None
    assistant_id = data.get("assistant_id")
    thread_id = data.get("thread_id")


    # Assistent ID is:
    assistant_id = assistant_id if assistant_id else await assist.create_assist(name, instructions, model, tools)
    
    # Thread ID:
    thread_id = thread_id if thread_id else await assist.create_tread()

    if user_content:
        # Кладём сообщение в канал:
        push_message = await assist.create_message(thread_id, user_content)
    else:
        return {"asist_id": assistant_id, "thread_id": thread_id, "system_message": "Missing message from user."}
    
    # Запускаем ассистента:
    run_id = await assist.run_assist(assistant_id, thread_id)

    return {"asist_id": assistant_id, "thread_id": thread_id, "run_id": run_id }




# Запрос ответа от запущенного Ассистента по треду:
async def oa_assist_retrieve(run_id: str, thread_id: str) -> tuple:
    '''Получение ответа от активного ассистента по указанному каналу (thread_id) и 
    идентификатору запуска (run_id)'''
    status, tool_calls = await assist.get_runs_threads(run_id, thread_id)
    return status, tool_calls



# Получение списка Ассистентов:
async def oa_assist_list():
    '''Получение списка Ассистентов'''
    list_assist = await assist.list_assist()
    return list_assist



# Удаление Ассистента:
async def oa_assist_del(assistant_id):
    '''Удаление ассистента по id'''
    response = await assist.delete_assist(assistant_id)
    return response



# Удаление Thread:
async def oa_thread_del(thread_id):
    '''Удаление Thread'''
    response = await assist.delete_tread(thread_id)
    return response






















    # # Ждём завершения run и получения ответа
    # while True:
    #     status, tool_calls = await assist.get_runs_threads(run_id, thread_id)
    #     if status == "requires_action":
    #         break
    #     if status == "completed":
    #         print("Ассистент ответил без вызова функций")
    #         exit()
    #     await asyncio.sleep(1)

    # return status, tool_calls

    
    #     # Запускаем функцию
    #     results = []

    #     for tool in tool_calls:
    #         func_name = tool.function.name
    #         args = json.loads(tool.function.arguments)

    #         if func_name == "add":
    #             a = args["a"]
    #             b = args["b"]
    #             result = a + b
    #         elif func_name == "multiply":
    #             a = args["a"]
    #             b = args["b"]
    #             result = a * b
    #         else:
    #             result = "Неизвестная функция"

    #         results.append({
    #             "tool_call_id": tool.id,
    #             "output": str(result)
    #         })


#     print(f"results: {results}")
#     print()


#     '''
#     results: [{'tool_call_id': 'call_39ij1bI4pO4rBPKrht4XaMZU', 'output': '13'}]

#     '''

#     # Возвращаем результат — ассистент вставит его в чат
#     output = client.beta.threads.runs.submit_tool_outputs(
#         thread_id=thread.id,
#         run_id=run.id,
#         tool_outputs=results
#     )

#     print(f"output: {output}")

#     '''
#     output: Run(id='run_9sKdh0WDALp88BRn6tk4JqVV', assistant_id='asst_UtCUnUUYRHlbDm8n86iFhcXl', cancelled_at=None, completed_at=None, created_at=1747744305, expires_at=1747744905, failed_at=None, incomplete_details=None, instructions='Ты помощник, который использует числовые функции от разработчика.', last_error=None, max_completion_tokens=None, max_prompt_tokens=None, metadata={}, model='gpt-4o', object='thread.run', parallel_tool_calls=True, required_action=None, response_format='auto', started_at=1747744307, status='queued', thread_id='thread_IiFVCPaW7GX1PwSIsmTbBlIP', tool_choice='auto', tools=[FunctionTool(function=FunctionDefinition(name='add', description='Сложить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function'), FunctionTool(function=FunctionDefinition(name='multiply', description='Умножить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=None, temperature=1.0, top_p=1.0, tool_resources={}, reasoning_effort=None)
    
#     '''

































    # # 1. Создаём ассистента с подключением двух функций, описываем каждую в Json:
    # assistant = client.beta.assistants.create(
    #     name="Математик",
    #     instructions="Ты помощник, который использует числовые функции от разработчика.", # 256,000 characters
    #     model="gpt-4o",
    #     tools=[
    #         {
    #             "type": "function",
    #             "function": {
    #                 "name": "add",
    #                 "description": "Сложить два числа", 
    #                 "parameters": {
    #                     "type": "object",
    #                     "properties": {
    #                         "a": {"type": "number"},
    #                         "b": {"type": "number"}
    #                     },
    #                     "required": ["a", "b"]
    #                 }
    #             }
    #         },
    #         {
    #             "type": "function",
    #             "function": {
    #                 "name": "multiply",
    #                 "description": "Умножить два числа",
    #                 "parameters": {
    #                     "type": "object",
    #                     "properties": {
    #                         "a": {"type": "number"},
    #                         "b": {"type": "number"}
    #                     },
    #                     "required": ["a", "b"]
    #                 }
    #             }
    #         }
    #     ]

    # )

    # print(f"Assistant: {assistant}")
    # print()
    # print(f"Assistant ID: {assistant.id}")

    # '''
    # Assistant: Assistant(id='asst_UtCUnUUYRHlbDm8n86iFhcXl', created_at=1747744303, description=None, instructions='Ты помощник, который использует числовые функции от разработчика.', metadata={}, model='gpt-4o', name='Математик', object='assistant', tools=[FunctionTool(function=FunctionDefinition(name='add', description='Сложить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function'), FunctionTool(function=FunctionDefinition(name='multiply', description='Умножить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function')], response_format='auto', temperature=1.0, tool_resources=ToolResources(code_interpreter=None, file_search=None), top_p=1.0, reasoning_effort=None)
    
    # Assistant ID: asst_UtCUnUUYRHlbDm8n86iFhcXl
    # '''


    # # Создаём thread канал:
    # thread = client.beta.threads.create()

    # print(f"Thread: {thread}")
    # print()
    # print(f"Thread ID: {thread.id}")

    # '''
    # Thread: Thread(id='thread_IiFVCPaW7GX1PwSIsmTbBlIP', created_at=1747744303, metadata={}, object='thread', tool_resources=ToolResources(code_interpreter=None, file_search=None))
    # Thread ID: thread_IiFVCPaW7GX1PwSIsmTbBlIP

    # '''


    # # Кладём сообщение  канал:
    # push_message = client.beta.threads.messages.create(
    #     thread_id=thread.id,
    #     role="user",
    #     content = user_content #"Найди сумму чисел 5 и 8"
    # )

    # print(f"Push_message: {push_message}")
    # print()

    # '''
    #  Push_message: Message(id='msg_nUn5hU4bGzZA888MPI9VquvE', assistant_id=None, attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value='Найди сумму чисел 5 и 8'), type='text')], created_at=1747744304, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='user', run_id=None, status=None, thread_id='thread_IiFVCPaW7GX1PwSIsmTbBlIP')


    # '''



    # # Запускаем ассистента:
    # run = client.beta.threads.runs.create( 
    #     thread_id=thread.id,
    #     assistant_id=assistant.id
    # )

    # print(f"run: {run}")
    # print()
    # print(f"run ID: {run.id}")


    # '''
    # run: Run(id='run_9sKdh0WDALp88BRn6tk4JqVV', assistant_id='asst_UtCUnUUYRHlbDm8n86iFhcXl', cancelled_at=None, completed_at=None, created_at=1747744305, expires_at=1747744905, failed_at=None, incomplete_details=None, instructions='Ты помощник, который использует числовые функции от разработчика.', last_error=None, max_completion_tokens=None, max_prompt_tokens=None, metadata={}, model='gpt-4o', object='thread.run', parallel_tool_calls=True, required_action=None, response_format='auto', started_at=None, status='queued', thread_id='thread_IiFVCPaW7GX1PwSIsmTbBlIP', tool_choice='auto', tools=[FunctionTool(function=FunctionDefinition(name='add', description='Сложить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function'), FunctionTool(function=FunctionDefinition(name='multiply', description='Умножить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=None, temperature=1.0, top_p=1.0, tool_resources={}, reasoning_effort=None)

    # run ID: run_9sKdh0WDALp88BRn6tk4JqVV    
    
    
    # '''


    # # Ждём завершения run и получения ответа
    # while True:
    #     run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    #     if run_status.status == "requires_action":
    #         break
    #     if run_status.status == "completed":
    #         print("Ассистент ответил без вызова функций")
    #         exit()
    #     time.sleep(1)


    # print(f"run_status: {run_status}")
    # print()
    # print(f"run_status status: {run_status.status}")

    # '''
    # run_status: Run(id='run_9sKdh0WDALp88BRn6tk4JqVV', assistant_id='asst_UtCUnUUYRHlbDm8n86iFhcXl', cancelled_at=None, completed_at=None, created_at=1747744305, expires_at=1747744905, failed_at=None, incomplete_details=None, instructions='Ты помощник, который использует числовые функции от разработчика.', last_error=None, max_completion_tokens=None, max_prompt_tokens=None, metadata={}, model='gpt-4o', object='thread.run', parallel_tool_calls=True, required_action=RequiredAction(submit_tool_outputs=RequiredActionSubmitToolOutputs(tool_calls=[RequiredActionFunctionToolCall(id='call_39ij1bI4pO4rBPKrht4XaMZU', function=Function(arguments='{"a":5,"b":8}', name='add'), type='function')]), type='submit_tool_outputs'), response_format='auto', started_at=1747744307, status='requires_action', thread_id='thread_IiFVCPaW7GX1PwSIsmTbBlIP', tool_choice='auto', tools=[FunctionTool(function=FunctionDefinition(name='add', description='Сложить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function'), FunctionTool(function=FunctionDefinition(name='multiply', description='Умножить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=None, temperature=1.0, top_p=1.0, tool_resources={}, reasoning_effort=None)

    # run_status status: requires_action
    
    # '''



    # # Обрабатываем вызов
    # tool_calls = run_status.required_action.submit_tool_outputs.tool_calls

    # print(f"tool_calls: {tool_calls}")
    # print()

    # '''
    # tool_calls: [RequiredActionFunctionToolCall(id='call_39ij1bI4pO4rBPKrht4XaMZU', function=Function(arguments='{"a":5,"b":8}', name='add'), type='function')]


    # '''


    # results = []

    # for tool in tool_calls:
    #     func_name = tool.function.name
    #     args = json.loads(tool.function.arguments)

    #     if func_name == "add":
    #         a = args["a"]
    #         b = args["b"]
    #         result = a + b
    #     elif func_name == "multiply":
    #         a = args["a"]
    #         b = args["b"]
    #         result = a * b
    #     else:
    #         result = "Неизвестная функция"

    #     results.append({
    #         "tool_call_id": tool.id,
    #         "output": str(result)
    #     })


    # print(f"results: {results}")
    # print()


    # '''
    # results: [{'tool_call_id': 'call_39ij1bI4pO4rBPKrht4XaMZU', 'output': '13'}]

    # '''

    # # Возвращаем результат — ассистент вставит его в чат
    # output = client.beta.threads.runs.submit_tool_outputs(
    #     thread_id=thread.id,
    #     run_id=run.id,
    #     tool_outputs=results
    # )

    # print(f"output: {output}")

    # '''
    # output: Run(id='run_9sKdh0WDALp88BRn6tk4JqVV', assistant_id='asst_UtCUnUUYRHlbDm8n86iFhcXl', cancelled_at=None, completed_at=None, created_at=1747744305, expires_at=1747744905, failed_at=None, incomplete_details=None, instructions='Ты помощник, который использует числовые функции от разработчика.', last_error=None, max_completion_tokens=None, max_prompt_tokens=None, metadata={}, model='gpt-4o', object='thread.run', parallel_tool_calls=True, required_action=None, response_format='auto', started_at=1747744307, status='queued', thread_id='thread_IiFVCPaW7GX1PwSIsmTbBlIP', tool_choice='auto', tools=[FunctionTool(function=FunctionDefinition(name='add', description='Сложить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function'), FunctionTool(function=FunctionDefinition(name='multiply', description='Умножить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=None, temperature=1.0, top_p=1.0, tool_resources={}, reasoning_effort=None)
    
    # '''