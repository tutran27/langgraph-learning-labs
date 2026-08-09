from .graph import create_graph
def main():

    print("========== Replaying a previous run ============")
    app = create_graph()

    config= {
        "configurable": {
            "thread_id": "test_writer_session"
        }
    }

    print("\n------------- Original response --------------")
    result = app.invoke(
        {
            "query": "Hãy viết một bài blog thật ngắn gọn, xúc tích, đầy đủ ý về phương pháp học tập hiệu quả",
        },
        config
    )
    print(f"📄 Original outline: \n{result['outline'][:500]}")
    print(f"📄 Original draft: \n{result['draft'][:500]}")
    
    print("\n------------- Replay response --------------\n")

    history=list(app.get_state_history(config))
    
    # Chọn checkpoint
    before_writer = next(
        (snapshot for snapshot in history if snapshot.next == ("generate_draft",)), None
    )
    print(f"Checkpoint: {before_writer.config}")
    if not before_writer:
        print("Không tìm thấy checkpoint")
        return

    result = app.invoke(
        None,
        before_writer.config
    )

    print(f"📄 Check outline: \n{result['outline'][:500]}")
    print(f"📄 Check draft: \n{result['draft'][:500]}")


if __name__=="__main__":
    main()
