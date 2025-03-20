from fastapi import FastAPI, UploadFile, File

from langchain_core.messages import HumanMessage

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from api.chat_openai_langchain import (
    State,
    call_model,
    summarize_history,
    transf_phrase_vers,
    print_update,
    should_continue,
)

app = FastAPI()

chain = None

@app.get("/")
async def root():
    print("Hello world")


@app.post("/alexandrin")
async def alexandrin(file: UploadFile = File(...)):
    if file.content_type != "text/plain":
        return {"error": "Only text files are supported"}
    content = await file.read()
    text = content.decode("utf-8")

    vers = transf_phrase_vers(text)

    return {"vers": vers}

@app.post("/init_conv")
async def init_conv(file: UploadFile = File(...)):
    global chain
    if file.content_type != "text/plain":
        return {"error": "Only text files are supported"}
    content = await file.read()
    text = content.decode("utf-8")

    chain = StateGraph(State)

    chain.add_node(
        "conversation", lambda input: call_model(state=input, conversation_summary=text)
    )


workflow.add_node(summarize_history)

workflow.add_edge(START, "conversation")

workflow.add_conditional_edges(
    "conversation",
    should_continue,
)

workflow.add_edge("summarize_history", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "4"}}
input_message = HumanMessage(content="Explique moi les métaphores du poème")
input_message.pretty_print()
for event in app.stream({"messages": [input_message]}, config, stream_mode="updates"):
    print_update(event)
