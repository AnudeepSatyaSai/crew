import os

def llm_explain(context, model='llama3', system_prompt=None):
    """
    Use a local LLM (via Ollama) to summarize and explain trade factors and recommendations.
    Requires Ollama running locally and the model pulled (e.g., 'ollama pull llama3').
    Returns a string summary.
    """
    try:
        import ollama
    except ImportError:
        raise ImportError("Please install the 'ollama' Python package: pip install ollama")

    prompt = f"Given the following analysis: {context}, summarize the main factors and provide a recommendation."
    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': prompt})
    response = ollama.chat(model=model, messages=messages)
    return response['message']['content'] 