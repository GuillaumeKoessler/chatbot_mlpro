import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()

prompt_template = """Réécris ce message de manière poétique : {message_fr}"""
prompt = PromptTemplate(template=prompt_template, input_variables=['message_fr'])

llm = ChatOpenAI(
    api_key=os.environ.get('API_KEY_OPENAI'),
    model=os.environ.get("MODEL_ID"),
    temperature=0.2
)
chain = prompt | llm 

print(chain.invoke("Salut, t'es jolie aujourd'hui, on dirait une fleur"))