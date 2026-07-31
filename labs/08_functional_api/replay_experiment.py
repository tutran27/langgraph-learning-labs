import sys
import os
import random

# Thêm thư mục gốc vào PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))

sys.path.insert(0, current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Reconfigure stdout to use utf-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

checkpointer = InMemorySaver()

@task
def roll_dice() -> int:
    val = random.randint(1, 6)
    print(f"  [Task Executing] Thực tế xúc xắc đổ ra: {val}")
    return val

@entrypoint(checkpointer=checkpointer)
def game_workflow(player: str) -> dict:
    dice_future = roll_dice()
    score = dice_future.result()
    
    # Interrupt để tạm dừng
    interrupt(f"Player {player} rolled {score}. Confirm results?")
    
    return {"player": player, "score": score}

def run_experiment():
    config = {"configurable": {"thread_id": "game-session-abc"}}
    
    print("====================================================")
    print("=== THỬ NGHIỆM RANH GIỚI BẤT ĐỊNH (REPLAY EXPERIMENT) ===")
    print("====================================================\n")
    
    print("Lượt 1 (Xúc xắc đổ thực sự, sau đó dừng ở interrupt):")
    res1 = game_workflow.invoke("Alice", config=config)
    interrupt_info = res1["__interrupt__"][0]
    print("Thông báo ngắt:", interrupt_info.value)
    
    print("\nLượt 2 (Resume, lấy kết quả xúc xắc từ Cache của checkpoint):")
    # roll_dice sẽ không thực sự chạy lại vì kết quả của task đã được lưu trong checkpoint của thread này
    res2 = game_workflow.invoke(Command(resume=True), config=config)
    print("Kết quả hoàn thành:", res2)
    
    # Trích xuất điểm từ chuỗi thông báo của lượt 1
    score_lượt_1 = int(interrupt_info.value.split("rolled ")[1].split(".")[0])
    
    assert res2["score"] == score_lượt_1, "Lỗi: Điểm số ngẫu nhiên bị thay đổi!"
    print("\n✅ Thành công: Điểm số trùng khớp hoàn toàn.")
    print("====================================================")

if __name__ == "__main__":
    run_experiment()
