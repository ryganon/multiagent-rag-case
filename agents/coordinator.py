from typing import Dict, Any, Optional
from agents.router_agent import RouterAgent
from agents.journey_agent import JourneyAgent
from agents.human_agent import HumanHandoffAgent
from agents.hf_agent import HFAgent
from models.schemas import ChatResponse, AgentDecision
import uuid

class AgentCoordinator:
    """Coordenador central do sistema multi-agentes"""

    def __init__(self):
        # Inicializar agentes
        self.router = RouterAgent()
        self.journey_agent = JourneyAgent()
        self.human_handoff_agent = HumanHandoffAgent()
        self.hf_agent = HFAgent()

        # Mapeamento de agentes
        self.agents = {            
            "journey": self.journey_agent,
            "human_handoff": self.human_handoff_agent,
            "hf_llama3": self.hf_agent
        }

    async def process_message(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> ChatResponse:
        """Processar mensagem através do sistema multi-agentes"""

        if not context:
            context = {}

        # Garantir session_id
        if 'session_id' not in context:
            context['session_id'] = str(uuid.uuid4())

        try:
            # 1. Rotear mensagem
            routing_decision = await self.router.route_message(message)
            
            # 2. Obter agente apropriado
            #selected_agent = self.agents.get(routing_decision.agent_name)
            selected_agent = self.hf_agent

            if not selected_agent:
                # Fallback para FAQ se agente não encontrado
                selected_agent = self.faq_agent
                routing_decision.agent_name = "faq"

            # 3. Adicionar informações de roteamento ao contexto
            context['routing_decision'] = routing_decision.dict()
            context['previous_agents_count'] = context.get('previous_agents_count', 0) + 1

            # 4. Processar com agente selecionado
            response = await selected_agent.process(message, context)

            return response

        except Exception as e:
            # Fallback em caso de erro
            return ChatResponse(
                response=f"Desculpe, ocorreu um erro inesperado: {str(e)}. Por favor, tente novamente.",
                agent_used="error_handler",
                session_id=context.get('session_id', str(uuid.uuid4())),
                escalated_to_human=True,
                sources=[]
            )

    async def health_check(self) -> Dict[str, bool]:
        """Verificar saúde de todos os agentes"""
        health_status = {}

        for agent_name, agent in self.agents.items():
            try:
                # Teste simples para verificar se o agente responde
                test_response = await agent.can_handle("test message")
                health_status[agent_name] = isinstance(test_response, (int, float))
            except:
                health_status[agent_name] = False

        health_status["router"] = True  # Router é sempre saudável
        return health_status

# Instância global do coordenador
agent_coordinator = AgentCoordinator()