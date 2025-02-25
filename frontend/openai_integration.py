import openai

# Função para consultar o modelo OpenAI com a nova API
def query_openai_model(model, prompt, temperature=1.0, max_tokens=150):
    response = openai.chat.completions.create(  # Usando a nova API de chat
        model=model,
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()
