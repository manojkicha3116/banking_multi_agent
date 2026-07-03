from google.adk.models.lite_llm import LiteLlm


class ModelManager:

    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = LiteLlm(
                model="ollama_chat/llama3:latest"
            )
        
        return cls._model