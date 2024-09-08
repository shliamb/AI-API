import openai

# Замените 'your-api-key' на ваш ключ API OpenAI
openai.api_key = 'your-api-key'




def upload_file_openai(path, purpose):
    # Открываем файл в бинарном режиме
    with open('path/to/your/file.txt', 'rb') as file:
        # Загружаем файл
        response = openai.File.create(
            file=file,
            purpose='fine-tune'  # или другой подходящий параметр в зависимости от вашего случая использования
        )

    print("Файл загружен:", response) # get id file
    return response




def question_about_file_openai(file_id, question):
    # ID вашего загруженного файла
    # file_id = 'file-xxxxxxxxxxxxxx'  # Замените на реальный ID вашего файла

    # Пример вопроса
    #question = "Какое основное содержание этого файла?"

    # Используем модель с указанием контекста из файла
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Укажите нужную модель
        messages=[
            {"role": "system", "content": "Вы помощник."},
            {"role": "user", "content": question},
            {"role": "user", "content": f"Вот содержимое моего файла: {file_id}"}
        ]
    )

    print("Ответ модели:", response['choices'][0]['message']['content'])
    return response