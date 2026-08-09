from langgraph.runtime import Runtime

from ..context import Context
from ..state import State



def retrieve_memory(state: State, runtime: Runtime[Context]):
    query = state["query"]
    user_id = runtime.context.user_id
    store=runtime.store
    retrieved_memories = store.search(
        namespace=("memories", user_id),
        query=query,
        limit=5,
    )

    return {
        "retrieved_memories": retrieved_memories
    }
