import re
import shutil
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

PASTA_BASE = Path("base")
PASTA_DB = "db"
COLECAO = "politicas"
MODELO_EMBEDDING = "text-embedding-3-small"

RUIDOS = [
    r"Empório da Música Manual de Políticas e Procedimentos",
    r"Página \d+",
]


def limpar_texto(texto: str) -> str:
    for padrao in RUIDOS:
        texto = re.sub(padrao, "", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)  # colapsa linhas em branco
    return texto.strip()


def carregar_politicas():
    # glob evita problema de acento (í)
    arquivos_pdf = list(PASTA_BASE.glob("*.pdf"))
    if not arquivos_pdf:
        return []

    paginas = []
    for arquivo in arquivos_pdf:
        for pagina in PyPDFLoader(str(arquivo)).load():
            pagina.page_content = limpar_texto(pagina.page_content)
            pagina.metadata["fonte"] = "manual_politicas"
            paginas.append(pagina)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " "],
        add_start_index=True,
    )
    return splitter.split_documents(paginas)


def criar_db():
    chunks = carregar_politicas()
    if not chunks:
        print(f"Nenhum PDF encontrado em '{PASTA_BASE}'.")
        return

    # Recria do zero para não duplicar documentos
    if Path(PASTA_DB).exists():
        shutil.rmtree(PASTA_DB)

    Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(model=MODELO_EMBEDDING),
        persist_directory=PASTA_DB,
        collection_name=COLECAO,
    )
    print(f"{len(chunks)} chunks do manual indexados em '{PASTA_DB}'.")


if __name__ == "__main__":
    criar_db()