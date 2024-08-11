from openai import OpenAI



def bot_response(query):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    completion = client.chat.completions.create(
    model="model-identifier",
    messages=[
        {"role": "system", "content": "Complete generation within 200 tokens, be very concise, less words, You are given message in a way that includes values that are relevant to the query and only talk about agriculture"},
        {"role": "user", "content": query}
    ],
    temperature=0.7,
    )

    return completion.choices[0].message

query = """Prompt": "How will climate change with increased rainfall affect apple cultivation?",
        "Soil Moisture": 59,
        "Temperature": 34,
        "Location": "Madhya Pradesh",
        "Previous Yield": 42.0,
        "Weather": "Rainy",
        "Season": "Summer",
        "Previous Harvested Crop": "Wheat"""
print(bot_response(query))