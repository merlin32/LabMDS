from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # necesar de bibliotecă, dar ignorat de Ollama
)

response = client.chat.completions.create(
    model="tinyllama",
    messages=[
        {"role": "user", "content": "How hard it is to build a rocket engine from scratch?"}
    ],
)
print(response.choices[0].message.content)
