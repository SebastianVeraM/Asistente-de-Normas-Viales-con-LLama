from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFacePipeline
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path

from langchain_classic.chains import RetrievalQA


CHUNK_SIZE = 1_000
CHUNK_OVERLAP = 150
RETRIEVAL_K = 3

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "Eres un asistente informativo sobre normas viales de la Ciudad de México. "
        "Responde en español y usa únicamente la información del CONTEXTO. "
        "Si el contexto no contiene la respuesta, dilo claramente y no inventes reglas. "
        "No presentes la respuesta como asesoría oficial ni como una determinación legal.\n\n"
        "CONTEXTO:\n{context}\n\n"
        "PREGUNTA: {question}\n\n"
        "RESPUESTA:"
    ),
)


def load_documents():
    project_dir = Path(__file__).resolve().parent
    pdf_paths = [
        project_dir / "Gaceta_Oficial_DF.pdf",
        project_dir / "Programa_Hoy_No_Circula.pdf",
        project_dir / "REGLAMENTO_DE_TRNSITO_DE_LA_CIUDAD_DE_MXICO_6.4.pdf",
    ]

    docs = []
    for pdf_path in pdf_paths:
        if not pdf_path.is_file():
            raise FileNotFoundError(f"No se encontró el documento: {pdf_path}")

        pages = PyPDFLoader(str(pdf_path)).load()
        if not any(page.page_content.strip() for page in pages):
            raise ValueError(
                f"No se pudo extraer texto de {pdf_path.name}. "
                "Si es un PDF escaneado, hará falta OCR."
            )
        docs.extend(pages)

    return docs


def create_vectorstore(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    if not chunks:
        raise ValueError(
            "No se generaron fragmentos de texto a partir de los PDFs.")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={"local_files_only": True},
    )
    return FAISS.from_documents(chunks, embeddings)


def build_rag(vectorstore):
    llm = HuggingFacePipeline.from_model_id(
        model_id="meta-llama/Llama-2-7b-chat-hf",
        task="text-generation",
        model_kwargs={"local_files_only": True},
        pipeline_kwargs={"max_new_tokens": 128, "do_sample": False},
    )
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(
            search_kwargs={"k": RETRIEVAL_K}
        ),
        chain_type="stuff",
        chain_type_kwargs={"prompt": QA_PROMPT},
        return_source_documents=True,
    )
    return qa
