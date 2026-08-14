from langgraph.runtime import Runtime

from ..context import Context
from ..state import State
from ..memory.namespaces import get_user_memory_namespace
from ..memory.policies import DEFAULT_MEMORY_SEARCH_LIMIT


def retrieve_memory(state: State, runtime: Runtime[Context]):
    query = state["query"]
    user_id = runtime.context.user_id
    store = runtime.store
    retrieved_memories = store.search(
        namespace=get_user_memory_namespace(user_id),
        query=query,
        limit=DEFAULT_MEMORY_SEARCH_LIMIT,
    )

    return {
        "retrieved_memories": retrieved_memories
    }

