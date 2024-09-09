# Base
import logging
import asyncio
# Google
import google.generativeai as genai
# Service
from keys import api_key_gemini, is_admin
from general_functions import calculation


genai.configure(api_key=api_key_gemini)


# Main Text Google Function
async def mod_gemini(description, image_path):

    try:
        username = description.get("username")
        user_content = description.get("user_content")
        system_content = description.get("system_content")
        model_name = description.get("model")
        # tools = description.get("tools")

        if not image_path:

            model = await genai.GenerativeModel(
                model_name = model_name,
                # tools = user_input.tools or None, # "tools": "code_execution",
                system_instruction = system_content or None
            )

        # if image_path:
        #     # Getting the base64 string
        #     base64_file = await encode_image(image_path)

        response = model.generate_content(user_content)

        # Tokens:
        if response:
            usage_metadata = response.usage_metadata
            total_token_count = usage_metadata.total_token_count
            logging.info(f"Gemini text in tokens: {str(model.count_tokens(user_content))}")
            logging.info(f"Gemini all text tokens: {str(response.usage_metadata)}")
        else:
            logging.error("No response from Google Gemini.")
            return {"response": "No response from Google Gemini."}
        
        model_version = model_name
        used_tokens = total_token_count

        # Calculation of money spent on tokens
        expenses = await calculation(username, model_version, used_tokens, input_data="text")

        return {"response": response.text, "expenses": expenses, "used_tokens": total_token_count}
    
    except Exception as e:
       logging.error(f"Error is: {e}")
       return {"Error:": e}






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

