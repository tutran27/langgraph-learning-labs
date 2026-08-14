from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from .context import Context
from .state import State
from .memory.store import create_memory_store
from .nodes.chat import chat_node
from .nodes.extract_memory import extract_memory
from .nodes.retrieve_memory import retrieve_memory
from .nodes.summarize_history import summarize_history
from .nodes.trim_messages import trim_messages


def create_graph():
    builder = StateGraph(State, context_schema=Context)

    builder.add_node("retrieve_memory", retrieve_memory)
    builder.add_node("trim_messages", trim_messages)
    builder.add_node("chat", chat_node)
    builder.add_node("extract_memory", extract_memory)
    builder.add_node("summarize_history", summarize_history)

    builder.add_edge(START, "retrieve_memory")
    builder.add_edge("retrieve_memory", "trim_messages")
    builder.add_edge("trim_messages", "chat")
    builder.add_edge("chat", "extract_memory")
    builder.add_edge("extract_memory", "summarize_history")
    builder.add_edge("summarize_history", END)

    return builder.compile(
        checkpointer=MemorySaver(),
        store=create_memory_store(),
    )


if __name__ == "__main__":
    app = create_graph()
    print("Graph compiled successfully!")

