import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from prompts import poesie

# Load environment variables from .env file

load_dotenv()


def transf_phrase_vers(phrase: str) -> str:
    """ """
    prompt_template = poesie.PROMPT_VERS
    prompt = PromptTemplate(template=prompt_template, input_variables=["phrase"])

    llm = ChatOpenAI(
        api_key=os.environ.get("API_KEY_OPENAI"),
        model=os.environ.get("MODEL_ID"),
        temperature=0.2,
    )
    chain = prompt | llm

    return chain.invoke(phrase).content
