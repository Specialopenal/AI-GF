import os
import pickle
import faiss
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import VectorStoreRetrieverMemory
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents import Document

INDEX_PATH    = "faiss.index"
METADATA_PATH = "faiss_meta.pkl"
VECTOR_DIM    = 384 
EMBEDDINGS    = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2",model_kwargs={"device": "cuda"})

def load_memory(k: int = 5) -> VectorStoreRetrieverMemory:
    if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
        index = faiss.read_index(INDEX_PATH)

        with open(METADATA_PATH, "rb") as f:
            meta = pickle.load(f)
        texts, ids = meta["texts"], meta["ids"]

        docs_dict = {
            doc_id: Document(page_content=text)
            for doc_id, text in zip(ids, texts)
        }
        docstore = InMemoryDocstore(docs_dict)

        index_to_id = {i: _id for i, _id in enumerate(ids)}

        vectorstore = FAISS(
            embedding_function=EMBEDDINGS,
            index=index,
            docstore=docstore,
            index_to_docstore_id=index_to_id,
        )
    else:
        index = faiss.IndexFlatL2(VECTOR_DIM)
        vectorstore = FAISS(
            embedding_function=EMBEDDINGS,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )

    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return VectorStoreRetrieverMemory(
        retriever=retriever,
        memory_key="history"
    )

def save_memory(vectorstore: FAISS):
    faiss.write_index(vectorstore.index, INDEX_PATH)

    texts = [doc.page_content for doc in vectorstore.docstore._dict.values()]
    ids   = list(vectorstore.docstore._dict.keys())
    with open(METADATA_PATH, "wb") as f:
        pickle.dump({"texts": texts, "ids": ids}, f)
