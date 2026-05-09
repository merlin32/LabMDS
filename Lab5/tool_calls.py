import json
import requests
import re
from openai import OpenAI
from types import SimpleNamespace

# Inițializare client
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# Definiția uneltelor (din fișierul tău)
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform arithmetic. Input: '10 * 5'.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_by_city",
            "description": "Get current weather for a city name.",
            "parameters": {
                "type": "object",
                "properties": {"city_name": {"type": "string"}},
                "required": ["city_name"],
            },
        },
    }
]

def fetch_weather(city_name):
    try:
        geo_res = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json")
        geo_data = geo_res.json()
        if "results" not in geo_data: return f"Orasul '{city_name}' nu a fost gasit."
        loc = geo_data["results"][0]
        w_res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={loc['latitude']}&longitude={loc['longitude']}&current_weather=true")
        w_data = w_res.json()
        return f"{w_data['current_weather']['temperature']}°C in {loc['name']}"
    except Exception as e: return f"Eroare: {str(e)}"

def execute_tool(name, args):
    if name == "calculate":
        try: return str(eval(args["expression"]))
        except: return "Eroare matematica."
    elif name == "get_weather_by_city":
        return fetch_weather(args["city_name"])
    return "Tool inexistent."

def run_agent():
    print("=== Sistem de Comparare: Plain vs Tool-Enabled ===")
    print("(Scrie 'exit' pentru a termina)")
    
    while True:
        user_input = input("\nTu: ").strip()
        if user_input.lower() in ["exit", "quit"]: break
        
        # --- PARTEA 1: MODELUL PLAIN (FĂRĂ TOOLS) ---
        # Aceasta este partea cerută pentru comparație
        plain_response = client.chat.completions.create(
            model="mistral",
            messages=[{"role": "user", "content": user_input}],
            temperature=0
        )
        print(f"\n[MODEL PLAIN]: {plain_response.choices[0].message.content}")

        # --- PARTEA 2: MODELUL CU TOOL CALLS ---
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Use tools for math or weather."},
            {"role": "user", "content": user_input}
        ]

        response = client.chat.completions.create(model="mistral", messages=messages, tools=tools, temperature=0)
        msg = response.choices[0].message
        tool_calls_to_process = []

        # Logica de detecție tool calls din codul tău
        if msg.tool_calls:
            tool_calls_to_process = msg.tool_calls
            messages.append(msg)
        elif msg.content and "[{" in msg.content:
            match = re.search(r'\[\s*\{.*\}\s*\]', msg.content, re.DOTALL)
            if match:
                try:
                    fake_calls = json.loads(match.group())
                    formatted_calls = [{"id": f"m_{i}", "type": "function", "function": {"name": c['name'], "arguments": json.dumps(c['arguments'])}} for i, c in enumerate(fake_calls)]
                    messages.append({"role": "assistant", "tool_calls": formatted_calls})
                    for tc in formatted_calls:
                        tool_calls_to_process.append(SimpleNamespace(id=tc["id"], function=SimpleNamespace(name=tc["function"]["name"], arguments=tc["function"]["arguments"])))
                except: pass

        # Execuție unelte dacă este cazul
        if tool_calls_to_process:
            for tc in tool_calls_to_process:
                res = execute_tool(tc.function.name, json.loads(tc.function.arguments))
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": res})

            final_res = client.chat.completions.create(
                model="mistral", 
                messages=messages + [{"role": "user", "content": "Provide the final answer based on tool results."}],
                temperature=0
            )
            print(f"[MODEL CU TOOLS]: {final_res.choices[0].message.content}")
        else:
            print(f"[MODEL CU TOOLS]: {msg.content}")

if __name__ == "__main__":
    run_agent()
