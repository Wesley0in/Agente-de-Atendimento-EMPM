# Agente de Atendimento — Empório da Música

Agente de atendimento em Python para a Empório da Música (desafio Artefact).
Responde sobre produtos, preços, pedidos e políticas da loja.

## Como rodar
Pré-requisitos: Python 3.11+ e uma chave da OpenAI.

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env          # coloque sua OPENAI_API_KEY
    python criar_db.py            # indexa o manual de políticas (1x)
    python main.py                # inicia o chat

## Arquitetura
Mensagem → Agente (function calling) → escolhe a ferramenta:
- buscar_produtos → pandas sobre products + categories + promotions
- consultar_pedido → pandas sobre orders + order_items + customers (com verificação)
- consultar_politicas → RAG (Chroma) sobre o manual em PDF

## Decisões técnicas
- **Abordagem híbrida:** Na primeira versão vetorizei os CSVs junto com o PDF, mas a busca semântica não conseguia filtrar por preço nem cruzar pedido com produto. Por isso separei: dados tabulares via pandas e RAG só para o manual.

- **LLM:** gpt-4o-mini — Optei por este modelo por conta do custo benefício de utilizar function calling, achei confiável.
- **Framework:** LangChain `create_agent` + LangGraph (memória).
- **RAG:** chunks de 800/100, limpeza de cabeçalho/rodapé, text-embedding-3-small.
- **Prompt:** persona e regras extraídas da seção 7 do manual.
- **Histórico:** em memória durante a sessão (InMemorySaver).
- **LGPD:** dados de clientes não indexados; pedido só com e-mail/telefone.

## Suposições e inconsistências encontradas nos dados
- Dois WhatsApps no manual (3341-4444 e 3321-4500).
- E-mail com acento em um trecho do manual.
- Promoções duplicadas por produto — usei apenas as ativas, maior desconto.

## Exemplos
Ver pasta `exemplos/`.

## Limitações e próximos passos
- Histórico não persiste após fechar o programa.
- Sem avaliação automatizada (faria um conjunto de perguntas/respostas esperadas).
- Busca por nome é textual simples (faria busca aproximada).
- Interface CLI (próximo passo: Streamlit / integração com WhatsApp).

## Uso de assistentes de código
Usei o Claude como revisor técnico e mentor: avaliação da primeira versão, identificação de que embedding não serve para dados tabulares, sugestão de arquitetura híbrida e esboços de código. Comecei com uma abordagem focada em utilizar embedding para toda a minha base de dados, vi que não funcionou e recorri ao claude para entender como poderia trabalhar com PDF e CSV sem perder nenhum conteúdo. Além do auxilio na arquitetura, o claude foi um ótimo mentor na hora de codar, aprendi conceitos que não iam além do meu conhecimento.