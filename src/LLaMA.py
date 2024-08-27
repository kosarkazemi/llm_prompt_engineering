from src.LanguageModel import LanguageModel

class LLaMA(LanguageModel):
    def __init__(self):
        super().__init__("LLaMA")

    def format_prompt(self, system_prompt, user_message):
        # Implement LLaMA specific prompt parsing
        prompt = f"<S> [INST] <<SYS>>" \
                f"{system_prompt}" \
                f"<</SYS>>" \
                f"{user_message} [/INST]"
        return prompt

    def call_model(self, prompt):
        return super().call_model(prompt)
