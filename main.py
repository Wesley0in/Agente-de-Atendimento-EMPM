import uuid
from agente import agente

config = {"configurable": {"thread_id": str(uuid.uuid4())}}
print("Empório da Música — digite 'sair' para encerrar.\n")
while (msg := input("Você: ").strip()).lower() not in ("sair", "exit"):
        r = agente.invoke({"messages": [{"role": "user", "content": msg}]}, config)
        for m in r["messages"]:
            for tc in getattr(m, "tool_calls", None) or []:
                print(f"  [ferramenta: {tc['name']} {tc['args']}]")
        print("\nEmpório:", r["messages"][-1].content, "\n")
    