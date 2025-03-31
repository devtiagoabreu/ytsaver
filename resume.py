import google.generativeai as genai
import dotenv 
import os

dotenv.load_dotenv(dotenv.find_dotenv())

genai.configure(api_key=os.getenv("API_KEY_GOOGLE_AI"))

model = genai.GenerativeModel("gemini-1.5-pro-latest")

response = model.generate_content("Qual o sentido da vida?")

##models = genai.list_models()
##for model in models:
##    print(model.name)

print(response.text)