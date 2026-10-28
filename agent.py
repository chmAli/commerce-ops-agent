import json
import anthropic
from tools import TOOLS, get_orders

MODEL = "claude-sonnet-5-5"
SYSTEM = ("You are an operations assistant for an online store. Today is 2026-10-28. "
          "Use tools to look at real data; never guess. Answer briefly with order ids and numbers.")

client = anthropic.Anthropic()

def run_tool(name, args):
    if name == "get_orders":
        return get_orders(**args)
    raise ValueError(f"unknown tool {name}")

def ask(question: str) -> str:
    messages = [{"role": "user", "content": question}]
    while True:
        r = client.messages.create(model=MODEL, max_tokens=1000, system=SYSTEM,
                                   tools=TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": r.content})
        if r.stop_reason != "tool_use":
            return "".join(b.text for b in r.content if b.type == "text")
        results = []
        for b in r.content:
            if b.type == "tool_use":
                print(f"-> {b.name}({b.input})")
                results.append({"type": "tool_result", "tool_use_id": b.id,
                                "content": json.dumps(run_tool(b.name, b.input))})
        messages.append({"role": "user", "content": results})

if __name__ == "__main__":
    print(ask("Which customer has the most open orders?"))