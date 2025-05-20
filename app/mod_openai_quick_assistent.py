import logging
from openai import OpenAI
import time
import json

from keys import API_KEY_OPENAI
from config import defoult_model_openai


client = OpenAI(api_key=API_KEY_OPENAI)




async def mod_openai_quick_assist(user_content:str) -> None:

    # 1. Создаём ассистента с подключением двух функций, описываем каждую в Json:
    assistant = client.beta.assistants.create(
        name="Математик",
        instructions="Ты помощник, который использует числовые функции от разработчика.",
        model="gpt-4o",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "add",
                    "description": "Сложить два числа", # max 512 characters
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number"},
                            "b": {"type": "number"}
                        },
                        "required": ["a", "b"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "multiply",
                    "description": "Умножить два числа",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number"},
                            "b": {"type": "number"}
                        },
                        "required": ["a", "b"]
                    }
                }
            }
        ]

    )

    print(f"Assistant: {assistant}")
    print()
    print(f"Assistant ID: {assistant.id}")



    # Создаём thread канал:
    thread = client.beta.threads.create()

    print(f"Thread: {thread}")
    print()
    print(f"Thread ID: {thread.id}")



    # Кладём сообщение  канал:
    push_message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content = user_content #"Найди сумму чисел 5 и 8"
    )

    print(f"Push_message: {push_message}")
    print()



    # Запускаем ассистента:
    run = client.beta.threads.runs.create( 
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    print(f"run: {run}")
    print()
    print(f"run ID: {run.id}")



    # Ждём завершения run и получения ответа
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status == "requires_action":
            break
        if run_status.status == "completed":
            print("Ассистент ответил без вызова функций")
            exit()
        time.sleep(1)


    print(f"run_status: {run_status}")
    print()
    print(f"run_status status: {run_status.status}")



    # Обрабатываем вызов
    tool_calls = run_status.required_action.submit_tool_outputs.tool_calls

    print(f"tool_calls: {tool_calls}")
    print()




    results = []

    for tool in tool_calls:
        func_name = tool.function.name
        args = json.loads(tool.function.arguments)

        if func_name == "add":
            a = args["a"]
            b = args["b"]
            result = a + b
        elif func_name == "multiply":
            a = args["a"]
            b = args["b"]
            result = a * b
        else:
            result = "Неизвестная функция"

        results.append({
            "tool_call_id": tool.id,
            "output": str(result)
        })


    print(f"results: {results}")
    print()


    # Возвращаем результат — ассистент вставит его в чат
    output = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=results
    )

    print(f"output: {output}")