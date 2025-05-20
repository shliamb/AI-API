import logging
from openai import OpenAI
import time
import json

from keys import API_KEY_OPENAI
from config import defoult_model_openai
from common_openai_assist import AssistOpenAI


client = OpenAI(api_key=API_KEY_OPENAI)





async def mod_openai_quick_assist(user_content:str) -> None:

    assist = AssistOpenAI(client)


    print(f"List assist: {assist.list_assist()}")

    # new_assist_id = assist.create_assist(name, instructions, model, tools)












# async def mod_openai_quick_assist(user_content:str) -> None:

#     # 1. Создаём ассистента с подключением двух функций, описываем каждую в Json:
#     assistant = client.beta.assistants.create(
#         name="Математик",
#         instructions="Ты помощник, который использует числовые функции от разработчика.", # 256,000 characters
#         model="gpt-4o",
#         tools=[
#             {
#                 "type": "function",
#                 "function": {
#                     "name": "add",
#                     "description": "Сложить два числа", 
#                     "parameters": {
#                         "type": "object",
#                         "properties": {
#                             "a": {"type": "number"},
#                             "b": {"type": "number"}
#                         },
#                         "required": ["a", "b"]
#                     }
#                 }
#             },
#             {
#                 "type": "function",
#                 "function": {
#                     "name": "multiply",
#                     "description": "Умножить два числа",
#                     "parameters": {
#                         "type": "object",
#                         "properties": {
#                             "a": {"type": "number"},
#                             "b": {"type": "number"}
#                         },
#                         "required": ["a", "b"]
#                     }
#                 }
#             }
#         ]

#     )

#     print(f"Assistant: {assistant}")
#     print()
#     print(f"Assistant ID: {assistant.id}")

#     '''
#     Assistant: Assistant(id='asst_UtCUnUUYRHlbDm8n86iFhcXl', created_at=1747744303, description=None, instructions='Ты помощник, который использует числовые функции от разработчика.', metadata={}, model='gpt-4o', name='Математик', object='assistant', tools=[FunctionTool(function=FunctionDefinition(name='add', description='Сложить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function'), FunctionTool(function=FunctionDefinition(name='multiply', description='Умножить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function')], response_format='auto', temperature=1.0, tool_resources=ToolResources(code_interpreter=None, file_search=None), top_p=1.0, reasoning_effort=None)
    
#     Assistant ID: asst_UtCUnUUYRHlbDm8n86iFhcXl
#     '''


#     # Создаём thread канал:
#     thread = client.beta.threads.create()

#     print(f"Thread: {thread}")
#     print()
#     print(f"Thread ID: {thread.id}")

#     '''
#     Thread: Thread(id='thread_IiFVCPaW7GX1PwSIsmTbBlIP', created_at=1747744303, metadata={}, object='thread', tool_resources=ToolResources(code_interpreter=None, file_search=None))
#     Thread ID: thread_IiFVCPaW7GX1PwSIsmTbBlIP

#     '''


#     # Кладём сообщение  канал:
#     push_message = client.beta.threads.messages.create(
#         thread_id=thread.id,
#         role="user",
#         content = user_content #"Найди сумму чисел 5 и 8"
#     )

#     print(f"Push_message: {push_message}")
#     print()

#     '''
#      Push_message: Message(id='msg_nUn5hU4bGzZA888MPI9VquvE', assistant_id=None, attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value='Найди сумму чисел 5 и 8'), type='text')], created_at=1747744304, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='user', run_id=None, status=None, thread_id='thread_IiFVCPaW7GX1PwSIsmTbBlIP')


#     '''



#     # Запускаем ассистента:
#     run = client.beta.threads.runs.create( 
#         thread_id=thread.id,
#         assistant_id=assistant.id
#     )

#     print(f"run: {run}")
#     print()
#     print(f"run ID: {run.id}")


#     '''
#     run: Run(id='run_9sKdh0WDALp88BRn6tk4JqVV', assistant_id='asst_UtCUnUUYRHlbDm8n86iFhcXl', cancelled_at=None, completed_at=None, created_at=1747744305, expires_at=1747744905, failed_at=None, incomplete_details=None, instructions='Ты помощник, который использует числовые функции от разработчика.', last_error=None, max_completion_tokens=None, max_prompt_tokens=None, metadata={}, model='gpt-4o', object='thread.run', parallel_tool_calls=True, required_action=None, response_format='auto', started_at=None, status='queued', thread_id='thread_IiFVCPaW7GX1PwSIsmTbBlIP', tool_choice='auto', tools=[FunctionTool(function=FunctionDefinition(name='add', description='Сложить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function'), FunctionTool(function=FunctionDefinition(name='multiply', description='Умножить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=None, temperature=1.0, top_p=1.0, tool_resources={}, reasoning_effort=None)

#     run ID: run_9sKdh0WDALp88BRn6tk4JqVV    
    
    
#     '''


#     # Ждём завершения run и получения ответа
#     while True:
#         run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
#         if run_status.status == "requires_action":
#             break
#         if run_status.status == "completed":
#             print("Ассистент ответил без вызова функций")
#             exit()
#         time.sleep(1)


#     print(f"run_status: {run_status}")
#     print()
#     print(f"run_status status: {run_status.status}")

#     '''
#     run_status: Run(id='run_9sKdh0WDALp88BRn6tk4JqVV', assistant_id='asst_UtCUnUUYRHlbDm8n86iFhcXl', cancelled_at=None, completed_at=None, created_at=1747744305, expires_at=1747744905, failed_at=None, incomplete_details=None, instructions='Ты помощник, который использует числовые функции от разработчика.', last_error=None, max_completion_tokens=None, max_prompt_tokens=None, metadata={}, model='gpt-4o', object='thread.run', parallel_tool_calls=True, required_action=RequiredAction(submit_tool_outputs=RequiredActionSubmitToolOutputs(tool_calls=[RequiredActionFunctionToolCall(id='call_39ij1bI4pO4rBPKrht4XaMZU', function=Function(arguments='{"a":5,"b":8}', name='add'), type='function')]), type='submit_tool_outputs'), response_format='auto', started_at=1747744307, status='requires_action', thread_id='thread_IiFVCPaW7GX1PwSIsmTbBlIP', tool_choice='auto', tools=[FunctionTool(function=FunctionDefinition(name='add', description='Сложить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function'), FunctionTool(function=FunctionDefinition(name='multiply', description='Умножить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=None, temperature=1.0, top_p=1.0, tool_resources={}, reasoning_effort=None)

#     run_status status: requires_action
    
#     '''



#     # Обрабатываем вызов
#     tool_calls = run_status.required_action.submit_tool_outputs.tool_calls

#     print(f"tool_calls: {tool_calls}")
#     print()

#     '''
#     tool_calls: [RequiredActionFunctionToolCall(id='call_39ij1bI4pO4rBPKrht4XaMZU', function=Function(arguments='{"a":5,"b":8}', name='add'), type='function')]


#     '''


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