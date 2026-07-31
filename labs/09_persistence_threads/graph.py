import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import StateGraph, START, END
from state import ConversationState
from nodes import chat_response
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

          
    
def create_graph():
    builder = StateGraph(ConversationState)
    builder.add_node("chat_response", chat_response)
    builder.add_edge(START, "chat_response")
    builder.add_edge("chat_response", END)

    
    return builder

if __name__ == "__main__":
    graph = create_graph()

    checkpointer = InMemorySaver()
    app = graph.compile(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": "thread-123"}}
    #Test
    state = {"query": "Hello", "messages": []}

    while True:
        user_input = input("User: ")
        if user_input in ["q", "exit", "quit", "bye"]:
            break
        state["query"] = user_input
        res=app.invoke(state, config)
        print(res['response'].content)
        