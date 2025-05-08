from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

client = OpenAI(api_key=openai_api_key)

response = client.responses.create(
    model="gpt-4.1", input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
