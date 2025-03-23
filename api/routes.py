from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse

from langchain_core.messages import HumanMessage

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from api.chat_openai_langchain import (
    State,
    call_model,
    summarize_history,
    transf_phrase_vers,
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

    poem = text

    workflow = StateGraph(State)
    workflow.add_node(
        "conversation", lambda input: call_model(state=input, conversation_summary=poem)
    )
    workflow.add_node(summarize_history)
    workflow.add_edge(START, "conversation")
    workflow.add_conditional_edges(
        "conversation",
        should_continue,
    )
    workflow.add_edge("summarize_history", END)
    memory = MemorySaver()
    chain = workflow.compile(checkpointer=memory)

    return {"poème": poem}


async def generate_stream(input_message, config, chain):
    for event in chain.stream(
        {"messages": [input_message]}, config, stream_mode="updates"
    ):
        yield event["conversation"]["messages"][0].content


@app.post("/update")
async def update(request: str = Form(...)):
    config = {"configurable": {"thread_id": "4"}}
    input_message = HumanMessage(content=request)
    return StreamingResponse(
        generate_stream(input_message, config, chain), media_type="text/plain"
    )
