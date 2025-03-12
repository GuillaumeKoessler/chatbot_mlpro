from fastapi import FastAPI, UploadFile, File
from api import chat_openai_langchain as co

app = FastAPI()


@app.get("/")
async def root():
    print("Hello world")


@app.post("/alexandrin")
async def alexandrin(file: UploadFile = File(...)):
    if file.content_type != "text/plain":
        return {"error": "Only text files are supported"}
    content = await file.read()
    text = content.decode("utf-8")

    vers = co.transf_phrase_vers(text)

    return {"vers": vers}
