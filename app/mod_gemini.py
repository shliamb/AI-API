# Base
import logging
# Google
import google.generativeai as genai
# Service
from keys import api_key_gemini, is_admin


genai.configure(api_key=api_key_gemini)



async def mod_gemini(username, user_input):
    try:
        model = genai.GenerativeModel(model_name=user_input.model, tools=user_input.tools or None, system_instruction=user_input.system_content or None) # "tools": "code_execution",
        response = model.generate_content(user_input.user_content)

        print(f"{model.count_tokens(user_input.user_content)} (in)")


        # Tokens:
        # Получаем метаданные использования
        usage_metadata = response.usage_metadata
        # Извлекаем только total_token_count
        total_token_count = usage_metadata.total_token_count

        # Выводим результат
        print(response.usage_metadata)
        print("\n\n")
        print("all:", total_token_count)
        print("\n\n")





        return {"response": response.text}
    
    except Exception as e:
       logging.error(f"Error is: {e}")
       return {"error:": e}






# import PIL.Image

# model = genai.GenerativeModel("gemini-1.5-flash")
# organ = PIL.Image.open(media / "organ.jpg")
# response = model.generate_content(["Tell me about this instrument", organ])
# print(response.text)





# # Upload the file.
# audio_file = genai.upload_file(path='sample.mp3')

# # Initialize a Gemini model appropriate for your use case.
# model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# # Create the prompt.
# prompt = "Summarize the speech."

# # Pass the prompt and the audio file to Gemini.
# response = model.generate_content([prompt, audio_file])

# # Print the response.
# print(response.text)



# Maximum file 20mb
# # Initialize a Gemini model appropriate for your use case.
# model = genai.GenerativeModel('models/gemini-1.5-flash')

# # Create the prompt.
# prompt = "Please summarize the audio."

# # Load the samplesmall.mp3 file into a Python Blob object containing the audio
# # file's bytes and then pass the prompt and the audio to Gemini.
# response = model.generate_content([
#     prompt,
#     {
#         "mime_type": "audio/mp3",
#         "data": pathlib.Path('samplesmall.mp3').read_bytes()
#     }
# ])

# # Output Gemini's response to the prompt and the inline audio.
# print(response.text)





# # Initialize a Gemini model appropriate for your use case.
# model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# # Create the prompt.
# prompt = "Generate a transcript of the speech."

# # Pass the prompt and the audio file to Gemini.
# response = model.generate_content([prompt, audio_file])

# # Print the transcript.
# print(response.text)




# # Set the `response_mime_type` to output JSON
# generation_config={"response_mime_type": "application/json"})=

