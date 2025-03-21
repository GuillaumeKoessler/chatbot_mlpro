import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langgraph.graph import MessagesState, END
from typing import Literal

from prompts import poesie, system

# Load environment variables from .env file

load_dotenv()


class State(MessagesState):
    history: str


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


def call_model(state: State, conversation_summary: str) -> dict:
    llm = ChatOpenAI(
        temperature=0.2,
        api_key=os.environ.get("API_KEY_OPENAI"),
        model=os.environ.get("MODEL_ID"),
    )

    history = state.get("history", "")
    if history:
        system_message = f"Summary of conversation earlier: {history}"
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        system_message = system.SYSTEM_PROMPT.format(conversation=conversation_summary)
        messages = [SystemMessage(content=system_message)] + state["messages"]
    response = llm.invoke(messages)

    return {"messages": [response]}


def summarize_history(state: State) -> dict:
    llm_summarize = ChatOpenAI(
        temperature=0.2,
        api_key=os.environ.get("API_KEY_OPENAI"),
        model=os.environ.get("MODEL_ID"),
    )

    history = state.get("history", "")
    if history:
        history_message = f"Summary of conversation earlier: {history}"
    else:
        history_message = "No conversation history available"
    message = state["messages"] + [HumanMessage(content=history_message)]
    response = llm_summarize.invoke(message)
    delete_message = [RemoveMessage(id=m.id) for m in state["message"][:-2]]
    return {"history": response.content, "messages": delete_message}


def should_continue(state: State) -> Literal["summarize_history", END]:
    message = state["messages"]
    if len(message) > 6:
        return "summarize_history"
    return END


def print_update(update: dict) -> None:
    for k, v in update.items():
        for m in v["messages"]:
            m.pretty_print()
            if "history" in v:
                print(v["history"])
