from shared.models import GroqLLMModel
from state import ConversationState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def convert_message(conversation):
    converted=[]
    for x in conversation:
        if isinstance(x,HumanMessage):
            converted.append(f"User: {x.content}")
        elif isinstance(x,AIMessage):
            converted.append(f"AI: {x.content}")
        elif isinstance(x,SystemMessage):
            converted.append(f"System: {x.content}")
        else:
            converted.append(f"{x.role}: {x.content}")
    return "\n".join(converted)

def chat_response(state: ConversationState) -> dict:
    model = GroqLLMModel()
    query = state.get("query")
    messages = state.get("messages")
    messages.append(HumanMessage(content=query))
    response = model.invoke(convert_message(messages))
    messages.append(AIMessage(content=response.content))
    return {"response": response,
            "messages": messages}
    
if __name__ == "__main__":
    state = {"query": "Hello", "messages": []}
    res=chat_response(state)['response'].content
    print(res)
    