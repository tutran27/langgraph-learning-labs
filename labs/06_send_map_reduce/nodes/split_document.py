import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from state import OverallState

def read_file_content(path: str) -> str:
    if not path or not os.path.exists(path):
        return ""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        reader = PdfReader(path)
        pages_text = [page.extract_text() for page in reader.pages if page.extract_text()]
        return "\n".join(pages_text)
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def split_document_node(state: OverallState):
    path = state.get("document_path", "")
    full_text = state.get("document", "")
    
    if path:
        full_text = read_file_content(path)
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_text(full_text)
    print(f"  --> [Split Document] Loaded document ({len(full_text)} chars), split into {len(chunks)} chunks.")
    
    return {
        "document": full_text,
        "chunks": chunks
    }

if __name__ == "__main__":
    input_init = {
        "document_path": "labs/06_send_map_reduce/sample_data/BÁO CÁO TÓM TẮT ĐỀ XUẤT DỰ ÁN.pdf"
    }
    result = split_document_node(input_init)
    print("============== Split Document Node ==============")
    print(f"Document length: {len(result.get('document', ''))} characters")
    print(f"Number of chunks: {len(result.get('chunks', []))}")