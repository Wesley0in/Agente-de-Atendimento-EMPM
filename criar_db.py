from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    CSVLoader,
    PyPDFDirectoryLoader,
)
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

PASTA_BASE = Path("base")
PASTA_DB = "db"


def carregar_documentos():
    documentos = []

    # Carrega e divide o texto dos PDFs em partes menores.
    loader_pdf = PyPDFDirectoryLoader(str(PASTA_BASE))
    documentos_pdf = loader_pdf.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )

    documentos.extend(splitter.split_documents(documentos_pdf))

    # Carrega cada linha dos CSVs como um documento.
    for arquivo in PASTA_BASE.rglob("*.csv"):
        loader_csv = CSVLoader(
            file_path=str(arquivo),
            autodetect_encoding=True,
        )
        documentos.extend(loader_csv.load())

    return documentos


def criar_db():
    documentos = carregar_documentos()

    if not documentos:
        print(f"Nenhum documento encontrado em {PASTA_BASE}.")
        return

    print(f"Total de documentos e chunks: {len(documentos)}")

    embeddings = OpenAIEmbeddings()

    Chroma.from_documents(
        documents=documentos,
        embedding=embeddings,
        persist_directory=PASTA_DB,
    )

    print(f"Base vetorial criada em '{PASTA_DB}'.")


if __name__ == "__main__":
    criar_db()