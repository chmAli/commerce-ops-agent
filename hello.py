import anthropic

MODEL = "claude-sonnet-5-5"  # check docs.claude.com → Models for the latest Sonnet ID
client = anthropic.Anthropic()

r = client.messages.create(
    model=MODEL,
    max_tokens=200,
    messages=[{"role": "user", "content": "In one line: what is an unfulfilled order?"}],
)
print(r.content[0].text)