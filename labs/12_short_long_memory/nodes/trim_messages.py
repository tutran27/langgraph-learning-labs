from ..state import State


def message_to_str(messages):
    res = ""
    for message in messages:
        res += f"{message.type}: {message.content}\n"
    return res


def trim_messages(state: State):
    messages = state["messages"]
    if len(messages) <= 8:
        return {"recent_messages": message_to_str(messages)}
    else:
        return {"recent_messages": message_to_str(messages[-8:])}


     