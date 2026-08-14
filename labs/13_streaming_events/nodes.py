import os
import asyncio
from typing import Dict, Any
from langchain_core.tools import tool
from langchain_core.callbacks.manager import adispatch_custom_event
from langchain_core.messages import SystemMessage, HumanMessage
from shared.models import GroqLLMModel
from shared.config import settings
from state import ResearchSubgraphState, ParentState

llm = GroqLLMModel()

@tool
async def web_search(query: str) -> str:
    """Search the web for information about a given query using Tavily Search."""
    tavily_key = os.getenv("TAVILY_API_KEY") or getattr(settings, "TAVILY_API_KEY", "")
    if tavily_key:
        try:
            from langchain_tavily import TavilySearch
            tavily_tool = TavilySearch(max_results=2, tavily_api_key=tavily_key)
            response = await tavily_tool.ainvoke({"query": query})
            
            results = response
            if isinstance(response, dict) and "results" in response:
                results = response["results"]
                
            if isinstance(results, list):
                snippets = []
                for r in results:
                    title = r.get("title", "")
                    content = r.get("content", "")
                    snippets.append(f"- [{title}] {content}")
                return "\n".join(snippets)
            return str(results)
        except Exception as e:
            return f"Tavily Search Error ({e}). Fallback data for '{query}'."
    
    await asyncio.sleep(1)
    return f"Kết quả trả về khi ở trạng thái Fallback cho '{query}'"

async def generate_queries_node(state: ResearchSubgraphState) -> Dict[str, Any]:
    topic = state.get("topic", "")
    queries = [
        f"{topic} overview and introduction",
        f"{topic} key features and architecture",
        f"{topic} challenges and limitations"
    ]
    return {
        "queries": queries,
        "progress": {"percentage": 20, "status": "Đã sinh các truy vấn tìm kiếm"}
    }

async def fetch_documents_node(state: ResearchSubgraphState) -> Dict[str, Any]:
    queries = state.get("queries", [])
    documents = []
    
    for i, query in enumerate(queries):
        doc = await web_search.ainvoke({"query": query})
        documents.append(doc)
        
        percent = 20 + int((i + 1) / len(queries) * 60)
        await adispatch_custom_event(
            "progress",
            {"percentage": percent, "status": f"Đã tìm kiếm xong: {query}"}
        )
        
    return {
        "documents": documents,
        "progress": {"percentage": 80, "status": "Hoàn tất tìm kiếm thông tin"}
    }

async def synthesize_node(state: ParentState) -> Dict[str, Any]:
    topic = state.get("topic", "")
    documents = state.get("documents", [])
    docs_text = "\n\n".join(documents)
    
    messages = [
        SystemMessage(content="Bạn là một trợ lý nghiên cứu thông tin chuyên nghiệp. Hãy viết báo cáo tóm tắt ngắn gọn và súc tích."),
        HumanMessage(content=f"Chủ đề nghiên cứu: {topic}\n\nDữ liệu thu thập được:\n{docs_text}")
    ]
    
    await adispatch_custom_event(
        "progress",
        {"percentage": 90, "status": "Bắt đầu tổng hợp báo cáo"}
    )
    
    chat_model = llm.groq_chat()
    response = await chat_model.ainvoke(messages)
    
    await adispatch_custom_event(
        "progress",
        {"percentage": 100, "status": "Hoàn tất tổng hợp báo cáo"}
    )
    
    return {
        "messages": [response],
        "progress": {"percentage": 100, "status": "Đã hoàn thành workflow"}
    }
