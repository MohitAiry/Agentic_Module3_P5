import ollama

# We define the model here so it's easy to change later if we download a new one
MODEL_NAME = "qwen2.5:7b-instruct-q8_0"

def call_llm(prompt: str) -> str:
    """
    Sends the prompt to our local Ollama model and gets the text response.
    """
    try:
        response = ollama.generate(
            model=MODEL_NAME,
            prompt=prompt,
            options={
                # CRITICAL: This stop token tells the LLM to pause.
                # When the LLM wants to use a tool, it outputs "Action: tool()".
                # It then expects an "Observation:", but we don't want the LLM 
                # to hallucinate the observation. We want our Python script to 
                # run the tool and provide the real observation.
                "stop": ["\nObservation:"]
            }
        )
        return response.get("response", "")
    
    except Exception as e:
        print(f" Error: Failed to connect to Ollama.")
        print(f"Make sure you have run 'ollama serve' in your terminal!")
        print(f"Details: {e}")
        return ""
