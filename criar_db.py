from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFDirectoryLoader,
    CSVLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

PASTA_BASE = Path("base")


def carregar_documentos():
    documentos = []

    # 1. Carregar PDFs
    loader_pdf = PyPDFDirectoryLoader(str(PASTA_BASE))
    documentos_pdf = loader_pdf.load()

    # 2. Dividir o texto dos PDFs em chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True
    )

    chunks_pdf = splitter.split_documents(documentos_pdf)
    documentos.extend(chunks_pdf)
    print(len(chunks_pdf))

    # 3. Carregar CSVs: uma linha por documento
    for arquivo in PASTA_BASE.rglob("*.csv"):
        loader_csv = CSVLoader(
            file_path=str(arquivo),
            autodetect_encoding=True,
        )

        documentos_csv = loader_csv.load()
        documentos.extend(documentos_csv)
        print(len(documentos_csv))

    return documentos

def vetorizar_chunks(chunks):
    db = Chroma.from_documents()


def criar_db():
    documentos = carregar_documentos()

    print(f"Total de documentos e chunks: {len(documentos)}")

    for documento in documentos[:3]:
        print(documento.page_content[:300])
        print(documento.metadata)


if __name__ == "__main__":
    criar_db()