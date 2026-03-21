# llm_client.py - Abstraction layer for LLM APIs

import config

class LLMClient:
    def __init__(self, model=config.DEFAULT_MODEL):
        self.model = model
        if model == "gemini":
            # Import and setup Gemini
            pass
        elif model == "claude":
            # Import and setup Claude
            pass
        else:
            raise ValueError("Unsupported model")

    def generate(self, prompt):
        if self.model == "gemini":
            # Call Gemini API
            pass
        elif self.model == "claude":
            # Call Claude API
            pass
        return "Response from " + self.model