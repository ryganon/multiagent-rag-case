from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from models.schemas import ChatMessage, ChatResponse
#from utils.huggingface_client import hf_client

class BaseAgent(ABC):
    """Classe base para todos os agentes"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    async def can_handle(self, message: str, context: Optional[Dict[str, Any]] = None) -> float:
        """
        Determinar se o agente pode lidar com a mensagem
        Retorna um score de 0.0 a 1.0
        """
        pass

    @abstractmethod
    async def process(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> ChatResponse:
        """Processar a mensagem e retornar resposta"""
        pass

    async def _generate_response(
        self, 
        prompt: str, 
        max_length: int = 512,
        temperature: float = 0.7
    ) -> str:
        """Gerar resposta usando Hugging Face"""
        try:
            response = await hf_client.generate_text(
                prompt=prompt,
                max_length=max_length,
                temperature=temperature
            )
            return response.strip()
        except Exception as e:
            return f"Desculpe, ocorreu um erro ao processar sua solicitação: {str(e)}"