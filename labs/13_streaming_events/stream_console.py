import asyncio
import sys
import os

from .graph import create_graph
from event_consumer import consume_events

# Mã màu ANSI
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

async def demo_stream_updates(app, inputs, config):
    print(f"\n{BOLD}=== 1. STREAM MODE: UPDATES (Chỉ stream các cập nhật của từng Node) ==={RESET}")
    async for update in app.astream(inputs, config, stream_mode="updates"):
        for node_name, state_update in update.items():
            print(f"[{BLUE}{node_name}{RESET}]: {state_update}")

async def demo_stream_values(app, inputs, config):
    print(f"\n{BOLD}=== 2. STREAM MODE: VALUES (Stream toàn bộ State sau mỗi bước) ==={RESET}")
    async for value in app.astream(inputs, config, stream_mode="values"):
        print(f"[{BLUE}State Snapshot{RESET}]: progress={value.get('progress')}, documents_count={len(value.get('documents', []))}")

async def demo_stream_messages(app, inputs, config):
    print(f"\n{BOLD}=== 3. STREAM MODE: MESSAGES (Chỉ stream các tin nhắn từ LLM) ==={RESET}")
    # stream_mode="messages" được dùng đặc biệt để stream các message chunk từ ChatModel
    async for msg, metadata in app.astream(inputs, config, stream_mode="messages"):
        node = metadata.get("langgraph_node", "unknown")
        # In các token nhận được
        if msg.content:
            print(f"[{GREEN}{node} message chunk{RESET}]: {msg.content}")

async def demo_stream_events(app, inputs, config):
    print(f"\n{BOLD}=== 4. STREAMING DETAILED EVENTS (Model tokens, Tools, Custom progress) ==={RESET}")
    # Sử dụng helper consume_events để xử lý astream_events v2
    async for event in consume_events(app, inputs, config):
        event_type = event["type"]
        
        if event_type == "node_start":
            print(f"\n{BLUE}▶ Bắt đầu Node: {event['node']}{RESET}")
        elif event_type == "node_end":
            print(f"{BLUE}■ Kết thúc Node: {event['node']}{RESET}")
            
        elif event_type == "tool_start":
            print(f"  {YELLOW}🛠 Tool Start: {event['tool']} | Input: {event['input']}{RESET}")
        elif event_type == "tool_end":
            print(f"  {YELLOW}🛠 Tool End: {event['tool']} | Output length: {len(str(event['output']))}{RESET}")
            
        elif event_type == "progress":
            progress = event["data"]
            print(f"  {CYAN}📈 Tiến trình: [{progress['percentage']}%] {progress['status']}{RESET}")
            
        elif event_type == "token":
            # Stream token từ Chat Model (in liên tiếp không xuống dòng)
            sys.stdout.write(f"{GREEN}{event['content']}{RESET}")
            sys.stdout.flush()
    print()

async def main():
    app = create_graph()
    inputs = {"topic": "Công nghệ Multi-Agent trong AI"}
    
    # Mỗi lần chạy cần một thread_id khác nhau để tránh đè trạng thái
    config_1 = {"configurable": {"thread_id": "thread_updates"}}
    config_2 = {"configurable": {"thread_id": "thread_values"}}
    config_3 = {"configurable": {"thread_id": "thread_messages"}}
    config_4 = {"configurable": {"thread_id": "thread_events"}}
    
    await demo_stream_updates(app, inputs, config_1)
    await demo_stream_values(app, inputs, config_2)
    # await demo_stream_messages(app, inputs, config_3)
    # await demo_stream_events(app, inputs, config_4)

if __name__ == "__main__":
    # Hỗ trợ Windows terminal hiển thị màu ANSI
    if sys.platform == "win32":
        os.system("color")
    asyncio.run(main())
