from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent
from models.schemas import ChatResponse
import uuid

class HumanHandoffAgent(BaseAgent):
    """Agente responsável por escalar atendimento para humanos"""

    def __init__(self):
        super().__init__(
            name="human_handoff",
            description="Agente que detecta quando escalar para atendimento humano"
        )

    async def can_handle(self, message: str, context: Optional[Dict[str, Any]] = None) -> float:
        """Verificar se deve escalar para humano"""
        escalation_indicators = [
            "falar com humano", "atendente", "pessoa real",
            "não consegui resolver", "problema complexo",
            "cancelar", "reembolso", "reclamação"
        ]

        message_lower = message.lower()
        score = 0.0

        for indicator in escalation_indicators:
            if indicator in message_lower:
                score += 0.3

        return min(score, 1.0)

    async def detect_escalation_needed(self, message: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """Detectar se escalação é necessária"""
        # Critérios para escalação
        escalation_keywords = [
            "urgente", "emergência", "bug crítico", "problema grave",
            "não funciona", "erro", "quebrado", "perdeu dinheiro"
        ]

        message_lower = message.lower()

        # Verificar palavras-chave de escalação
        for keyword in escalation_keywords:
            if keyword in message_lower:
                return True

        # Verificar frustração (múltiplos pontos de interrogação/exclamação)
        if "???" in message or "!!!" in message:
            return True

        # Verificar se já passou por múltiplos agentes sem resolução
        if context and context.get('previous_agents_count', 0) > 2:
            return True

        return False

    async def process(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> ChatResponse:
        """Processar escalação para humano"""
        return ChatResponse(
            response="response_message",
            agent_used="none",
            session_id="request.session_id"
        )