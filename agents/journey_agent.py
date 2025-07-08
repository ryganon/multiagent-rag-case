from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent
from models.schemas import ChatResponse, JourneyInfo
#from database.user_system import user_system
import uuid
import json

class JourneyAgent(BaseAgent):
    """Agente especializado em Hotmart Journey com Function Calling"""

    def __init__(self):
        super().__init__(
            name="journey",
            description="Agente especializado em questões do Stars e Legacy"
        )

    async def can_handle(self, message: str, context: Optional[Dict[str, Any]] = None) -> float:
        """Verificar se a mensagem é sobre Journey"""
        journey_keywords = ["journey", "stars", "legacy", "elegível", "benefícios", "tier"]
        message_lower = message.lower()

        score = 0.0
        for keyword in journey_keywords:
            if keyword in message_lower:
                score += 0.2

        return min(score, 1.0)

    async def process(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> ChatResponse:
        
        """Processar pergunta sobre Journey"""
        return ChatResponse(
            response="response_message",
            agent_used="none",
            session_id="request.session_id"
        )