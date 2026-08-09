from .graph import create_graph

def create_branch(app, base_checkpoint, update_values, as_node=None):
    fork_config=app.update_state(
        config=base_checkpoint.config,
        values=update_values,
        as_node=as_node
    )
    result=app.invoke(None,fork_config)
    return result

def main():
    print("============= TẠO NHÁNH =============\n")
    app=create_graph()
    config={"configurable": {"thread_id": "test_writer_session"}}
    query="Đoạn văn miêu tả con chó"

    print("----------- RUN BAN ĐẦU ----------")
    result_origin=app.invoke({"query":query},config)
    print(f"📄 Outline: \n{result_origin['outline'][:500]}")
    print(f"📄 Final text: \n{result_origin['final_text']}")

    print("\n------------ TẠO NHÁNH A ------------\n")
    history=list(app.get_state_history(config))
    before_draft = next(snapshot for snapshot in history if snapshot.next == ("generate_draft",))
    print(f"📍[LOG] before_draft checkpoint: {before_draft.config}")
    print(f"💻[LOG] before_draft values: {before_draft.values}")

    outline_original = before_draft.values.get("outline", "")
    
    branch_A_values={"outline": outline_original + "\nLưu ý chỉ 3 câu ngắn gọn thôi nhé"}
    branch_A_result = create_branch(
        app,
        base_checkpoint=before_draft,
        update_values=branch_A_values,
        as_node="generate_outline"
    )
    print("\n------------- NHÁNH A ------------\n")
    print(f"📄 Outline: \n{branch_A_result['outline'][:500]}")
    print(f"📄 Final text: \n{branch_A_result['final_text']}")

    print("\n------------ TẠO NHÁNH B ------------\n")
    branch_B_values={
        "outline": outline_original + "\n Tôi cần 5 câu ngắn gọn và viết theo kiểu gạch đầu dòng    "
    }
    branch_B_result=create_branch(
        app,
        base_checkpoint=before_draft,
        update_values=branch_B_values,
        as_node="generate_outline"
    )
    print("\n------------- NHÁNH B ------------\n")
    print(f"📄 Outline: \n{branch_B_result['outline'][:500]}")
    print(f"📄 Final text: \n{branch_B_result['final_text']}")
       
if __name__ == "__main__":
    main()