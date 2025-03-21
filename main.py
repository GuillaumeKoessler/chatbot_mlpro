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

poem = transf_phrase_vers(
    "Depuis le temps que nous partageons notre amour sans aucun nuage, je me suis rendu compte à quel point tu comptais pour moi. C'est à tes côtés que je veux construire ma vie, que nous avancions main dans la main."
)
print(poem)

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
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "4"}}
input_message = HumanMessage(content="Explique moi les métaphores du poème")
input_message.pretty_print()
for event in app.stream({"messages": [input_message]}, config, stream_mode="updates"):
    print_update(event)
