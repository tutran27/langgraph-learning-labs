from .graph import create_graph

def main():
    app = create_graph()

    config = {
        "configurable": {
            "thread_id": "test_writer_session"
        }
    }

    print("\n============= NHÁNH BAN ĐẦU =============\n")
    result_origin = app.invoke(
        {
            "query": "Hãy viết một bài blog thật ngắn gọn, xúc tích, đầy đủ ý về phương pháp học tập hiệu quả"
        },
        config
    )
    print(f"📄 Original outline: \n{result_origin['outline'][:500]}\n")
    print(f"📄 Original draft: \n{result_origin['draft'][:500]}\n")

    print("\n============= NHÁNH A ============\n")

    print("----------- Get history ----------\n")
    history = list(app.get_state_history(config))
    if not history:
        print("Không tìm thấy history")
        return
    
    before_writer = next((snapshot for snapshot in history if snapshot.next == ("generate_draft",)), None)
    if not before_writer:
        print("Không tìm thấy snapshot")
        return
    
    print(f"📍[LOG] Checkpoint: {before_writer.config}\n")
    print(f"💻[LOG] Before writer checkpoint values: {before_writer.values}")
    
    fork_config = app.update_state(
        config=before_writer.config,
        values={
            "outline": "Tôi muốn thay đổi outline thành một dàn ý chi tiết về chủ đề: Tác động của AI đến giáo dục"
        },
        as_node="generate_outline" # Xem update trên như kết quả đầu ra của node "generate_outline"
    )
    print(f"💻[LOG] App state after update_state: {app.get_state(config).values}")

    print(f"💻[LOG] Fork config: {fork_config}")
    
    fork_response=app.invoke(None, fork_config)
    print("\n------------- Fork A --------------\n")
    print(f"📄 Fork outline: \n{fork_response['outline'][:500]}")
    print(f"📄 Fork draft: \n{fork_response['draft'][:500]}")

if __name__ == "__main__":
    main()