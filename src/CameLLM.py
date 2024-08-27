from src.LanguageModel import LanguageModel

class CameLLM(LanguageModel):
    def __init__(self):
        super().__init__("CameLLM")
        self.field_name = "Answer CameLLM"

    def format_prompt(self, system_prompt, user_message):
        # Implement CameLLM specific prompt parsing
        prompt = f"<S>### System prompt" \
                f"{system_prompt}" \
                f"### User Message" \
                f"{user_message}"

        return prompt

    def call_model(self, prompt):
        return super().call_model(prompt)