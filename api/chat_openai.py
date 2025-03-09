import os
from dotenv import load_dotenv

from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    api_key=os.environ.get('API_KEY_OPENAI')
)

completion = client.chat.completions.create(
  model=os.environ["MODEL_ID"],
  messages=[
    {"role": "developer", "content": "Tu es un assistant pour le code en python"},
    {"role": "user", "content": "Bonjour assistant !"}
  ]
)

print(completion.choices[0].message)