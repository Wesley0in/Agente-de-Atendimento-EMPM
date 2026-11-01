from langchain.tools import tool

@tool
def buscar_produtos(termo: str = "", categoria: str = "", preco_max: float | None = None) -> str:
    """Busca instrumentos no catálogo (preço, estoque, promoção).
    Use para perguntas sobre produtos, preços, disponibilidade ou faixa de preço."""
    df = produtos[produtos.status != "discontinued"]
    if termo: df = df[df.name.str.contains(termo, case=False)]
    if categoria: df = df[df.categoria.str.contains(categoria, case=False)]
    if preco_max: df = df[df.preco_final <= preco_max]
    return df[["name","price_brl","discount_percent","preco_final","stock_quantity","status"]].head(15).to_string()

@tool
def consultar_pedido(order_id: int, email_ou_telefone: str) -> str:
    """Consulta status, rastreio e itens de um pedido. Exige número do pedido
    e e-mail ou telefone do cliente para verificação."""
    ...  # valida o cliente antes de retornar (LGPD)

@tool
def consultar_politicas(pergunta: str) -> str:
    """Consulta o manual da loja: horários, endereço, pagamento, trocas,
    devoluções, frete, garantia, promoções."""
    ...  # Chroma, só com o PDF