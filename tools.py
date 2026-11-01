import re
import unicodedata
from typing import Literal
from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dados import produtos, pedidos, itens, clientes
from criar_db import PASTA_DB, COLECAO, MODELO_EMBEDDING

_db = Chroma(persist_directory=PASTA_DB, collection_name=COLECAO,
             embedding_function=OpenAIEmbeddings(model=MODELO_EMBEDDING))

def _digitos(s): return re.sub(r"\D", "", str(s))

def _norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)

Categoria = Literal["Violões", "Guitarras", "Baixos", "Baterias e Percussão",
                    "Teclados e Pianos", "Ukuleles"]

@tool
def buscar_produtos(termo: str = "", categoria: Categoria | None = None,
                    preco_max: float | None = None, apenas_promocao: bool = False) -> str:
    """Busca instrumentos no catálogo (preço, estoque, promoção).
    Use para perguntas sobre produtos, preços, disponibilidade, faixa de preço ou promoções.
    - termo: marca ou modelo (ex: 'Takamine', 'Yamaha C40'). NÃO use para tipo de instrumento.
    - categoria: tipo de instrumento.
    - apenas_promocao: True para listar só produtos com promoção ativa."""
    df = produtos
    if termo:
        t = _norm(termo)
        df = df[df.name.map(_norm).str.contains(t) | df.description.map(_norm).str.contains(t)]
    if categoria: df = df[df.categoria.map(_norm) == _norm(categoria)]
    if preco_max: df = df[df.preco_final <= preco_max]
    if apenas_promocao: df = df[df.discount_percent.notna()]
    if df.empty: return "Nenhum produto encontrado com esses filtros."
    return df[["name","categoria","price_brl","discount_percent","preco_final",
               "stock_quantity","status"]].head(20).to_string()

@tool
def consultar_pedido(order_id: int, email_ou_telefone: str) -> str:
    """Consulta status, rastreio e itens de um pedido. Exige o número do pedido
    e o e-mail ou telefone do cliente para verificação de identidade."""
    p = pedidos[pedidos.order_id == order_id]
    if p.empty:
        return "Pedido não encontrado."
    p = p.iloc[0]
    c = clientes[clientes.customer_id == p.customer_id].iloc[0]

    ident = email_ou_telefone.strip().lower()
    d = _digitos(ident)
    if ident != c.email.lower() and not (len(d) >= 8 and _digitos(c.phone).endswith(d)):
        return "Dados de verificação não conferem. Não informe nada sobre o pedido."

    prods = ", ".join(f"{r.quantity}x {r['name']}" for _, r in itens[itens.order_id == order_id].iterrows())
    return (f"Pedido {order_id} | status: {p.status} | data: {p.order_date} | total: R$ {p.total_brl} | "
            f"pagamento: {p.payment_method} | rastreio: {p.tracking_code} | "
            f"previsão: {p.estimated_delivery} | obs: {p.notes} | itens: {prods}")

@tool
def consultar_politicas(pergunta: str) -> str:
    """Consulta o manual da loja: horários, endereço, contato, formas de pagamento,
    parcelamento, trocas, devoluções, frete, garantia e regras de promoção."""
    docs = _db.similarity_search(pergunta, k=4)
    return "\n\n---\n\n".join(d.page_content for d in docs)