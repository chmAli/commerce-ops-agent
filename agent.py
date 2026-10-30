import json, sys
import anthropic
from tools import TOOLS, FUNCTIONS

MODEL = "claude-sonnet-5-5"
SYSTEM = ("You are an operations assistant for an online store. Today is 2026-10-28. "
          "Use tools to look at real data; never guess. "
          "For counts, totals and dates, use the numbers the tools return; never count or calculate yourself. "
          "Answer briefly with order ids and numbers.")

client = anthropic.Anthropic()

def run_tool(name, args):
    if name not in FUNCTIONS:
        return {"error": f"unknown tool {name}"}
    return FUNCTIONS[name](**args)

def ask(question: str, trace: list | None = None, max_steps: int = 10) -> str:
    messages = [{"role": "user", "content": question}]
    for _ in range(max_steps):
        r = client.messages.create(model=MODEL, max_tokens=1000, system=SYSTEM,
                                   tools=TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": r.content})
        if r.stop_reason != "tool_use":
            return "".join(b.text for b in r.content if b.type == "text")
        results = []
        for b in r.content:
            if b.type == "tool_use":
                print(f"-> {b.name}({b.input})")
                if trace is not None:
                    trace.append((b.name, b.input))
                result = run_tool(b.name, b.input)
                print(f"   <- {json.dumps(result, default=str)[:120]}")
                results.append({"type": "tool_result", "tool_use_id": b.id,
                                "content": json.dumps(result, default=str)})
        messages.append({"role": "user", "content": results})
    return "Stopped: too many tool calls without an answer."

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Which orders are unfulfilled for more than 3 days, and how many days each?"
    print(ask(question))