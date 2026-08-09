from ..state import State

def message_to_str(messages):
    str=""
    for message in messages:
        str+=f"{message.type}: {message.content}\n"
    return str
    
def trim_messages(state: State):
    messages=state["messages"]
    if len(messages) <= 8:
        return {"recent_messages": message_to_str(messages)}
    else:
        return {"recent_messages": message_to_str(messages[-8:])}

     