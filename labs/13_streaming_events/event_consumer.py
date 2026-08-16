from typing import AsyncIterator, Any, Dict

async def consume_events(app: Any, inputs: Dict[str, Any], config: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
    async for event in app.astream_events(inputs, config, version="v2"):
        kind = event["event"]
        name = event["name"]
        
        if kind == "on_chat_model_stream":
            chunk = event["data"].get("chunk")
            if chunk and hasattr(chunk, "content") and chunk.content:
                yield {
                    "type": "token",
                    "content": chunk.content
                }
                
        elif kind == "on_tool_start":
            yield {
                "type": "tool_start",
                "tool": name,
                "input": event["data"].get("input")
            }
        elif kind == "on_tool_end":
            yield {
                "type": "tool_end",
                "tool": name,
                "output": event["data"].get("output")
            }
            
        elif kind == "on_chain_start":
            tags = event.get("tags", [])
            metadata = event.get("metadata", {})
            if "graph:step" in tags or "langgraph_node" in metadata:
                node_name = metadata.get("langgraph_node", name)
                yield {
                    "type": "node_start",
                    "node": node_name,
                    "is_subgraph": "langgraph_subgraph" in metadata or "research" in node_name
                }
        elif kind == "on_chain_end":
            tags = event.get("tags", [])
            metadata = event.get("metadata", {})
            if "graph:step" in tags or "langgraph_node" in metadata:
                node_name = metadata.get("langgraph_node", name)
                yield {
                    "type": "node_end",
                    "node": node_name,
                    "output": event["data"].get("output")
                }
                
        elif kind == "on_custom_event":
            if name == "progress":
                yield {
                    "type": "progress",
                    "data": event["data"]
                }
