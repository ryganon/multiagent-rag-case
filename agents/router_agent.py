from typing import List, Dict, Any, Optional
from agents.base_agent import BaseAgent
from models.schemas import AgentDecision
import re

class RouterAgent(BaseAgent):
    """Agente responsável por rotear mensagens para agentes especializados"""

    def __init__(self):
        super().__init__(
            name="router", 
            description="Agente roteador que direciona mensagens para agentes especializados"
        )

        # Palavras-chave para diferentes tipos de consulta
        self.journey_keywords = [
            "journey", "stars", "legacy", "hotmart journey", 
            "programa", "benefícios", "elegível", "elegibilidade",
            "tier", "nível", "status", "faturamento"
        ]

        self.human_handoff_keywords = [
            "falar com humano", "atendente", "pessoa real", "não entendi",
            "problema urgente", "reclamação", "cancelar", "reembolso",
            "suporte técnico", "bug", "erro grave"
        ]

    async def can_handle(self, message: str, context: Optional[Dict[str, Any]] = None) -> float:
        """Router sempre pode lidar com mensagens"""
        return 1.0

    async def route_message(self, message: str) -> AgentDecision:
        """Determinar qual agente deve processar a mensagem"""
        message_lower = message.lower()

        # Verificar se deve escalar para humano
        human_score = self._calculate_human_handoff_score(message_lower)
        if human_score > 0.7:
            return AgentDecision(
                agent_name="human_handoff",
                confidence=human_score,
                reasoning="Mensagem indica necessidade de atendimento humano"
            )

        # Verificar se é sobre Journey
        journey_score = self._calculate_journey_score(message_lower)        
        if journey_score > 0.6:
            return AgentDecision(
                agent_name="journey",
                confidence=journey_score,
                reasoning="Mensagem relacionada ao Hotmart Journey"
            )

        # Por padrão, usar agente FAQ
        return AgentDecision(
            agent_name="faq",
            confidence=0.8,
            reasoning="Consulta geral - direcionando para base de conhecimento"
        )

    def _calculate_journey_score(self, message: str) -> float:
        """Calcular score para agente Journey"""
        score = 0.0
        for keyword in self.journey_keywords:
            if keyword in message:
                score += 0.2
        return min(score, 1.0)

    def _calculate_human_handoff_score(self, message: str) -> float:
        """Calcular score para escalação humana"""
        score = 0.0
        for keyword in self.human_handoff_keywords:
            if keyword in message:
                score += 0.3

        # Detectar frustração ou múltiplas perguntas
        if "???" in message or "!!!" in message:
            score += 0.2

        return min(score, 1.0)

    async def process(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentDecision:
        """Processar roteamento"""
        return await self.route_message(message)