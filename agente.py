from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from tools import buscar_produtos, consultar_pedido, consultar_politicas
from prompts import SYSTEM_PROMPT

agente = create_agent(model="openai:gpt-4o-mini",
    tools=[buscar_produtos, consultar_pedido, consultar_politicas],
    system_prompt=SYSTEM_PROMPT, checkpointer=InMemorySaver())