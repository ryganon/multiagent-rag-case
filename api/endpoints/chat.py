# /api/endpoints/chat.py
from fastapi import APIRouter, HTTPException, Body
from models.schemas import ChatRequest, ChatResponse 
from agents.coordinator import AgentCoordinator 

router = APIRouter()
agent_coordinator = AgentCoordinator()

@router.post("/chat", response_model=ChatResponse)
async def handle_chat_message(request: ChatRequest):
    """
    Endpoint principal de conversação.
    Recebe uma mensagem do usuário, junto com seu ID de sessão,
    e a direciona para o sistema multi-agentes para obter uma resposta.
    """
    try:
        
        # A lógica de negócio é delegada ao coordenador de agentes
        response_message, source_agent = await agent_coordinator.process_message(
            #user_id=request.user_id,
            #session_id=request.session_id,
            message=request.message            
        )
        return {"resposta": response_message,
                "agente": source_agent}
    
    except Exception as e:
        # Tratamento de erro para a camada de API
        raise HTTPException(status_code=500, detail=str(e))
