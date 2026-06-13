import ollama

MODEL_NAME = "qwen2.5:7b-instruct-q8_0"

def call_llm(prompt: str) -> str:
    """Calls local Ollama instance"""
    try:
        response = ollama.generate(
            model=MODEL_NAME,
            prompt=prompt,
            options={
                "stop": ["\nObservation:"]
            }
        )
        return response.get("response", "")
    except Exception as e:
        print(f"Failed to connect to Ollama: {e}")
        return ""
