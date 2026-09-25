from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.document_loaders import PyPDFLoader


def load_documents():
    loaders = [
        PyPDFLoader("data/hoy_no_circula.pdf"),
        PyPDFLoader("data/reglamento_transito_cdmx.pdf"),
        PyPDFLoader("data/contingencias_ambientales.pdf")
    ]
    docs = []
    for loader in loaders:
        docs.extend(loader.load())
    return docs


def create_vectorstore(docs):
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore


def build_rag(vectorstore):
    llm = HuggingFacePipeline.from_model_id(
        model_id="meta-llama/Llama-2-7b-chat-hf",
        task="text-generation",
        model_kwargs={"temperature": 0.2, "max_length": 512}
    )
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff"
    )
    return qa
