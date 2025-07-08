from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    """Roles possíveis para mensagens"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    """Modelo para mensagens de chat"""
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)

class ChatRequest(BaseModel):
    """Modelo para requisições de chat"""
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    """Modelo para respostas de chat"""
    response: str
    agent_used: str
    session_id: str
    escalated_to_human: bool = False
    journey_info: Optional[Dict[str, Any]] = None
    sources: Optional[List[str]] = None

class UserProfile(BaseModel):
    """Modelo para perfil do usuário"""
    user_id: str
    email: str
    total_revenue: float = 0.0
    account_status: str = "active"
    registration_date: datetime
    last_purchase_date: Optional[datetime] = None
    journey_eligible: bool = False

class JourneyInfo(BaseModel):
    """Informações sobre o Hotmart Journey"""
    user_id: str
    total_revenue: float
    is_eligible: bool
    tier: str  # "none", "stars", "legacy"
    benefits: List[str]
    next_tier_requirement: Optional[float] = None

class AgentDecision(BaseModel):
    """Decisão do agente roteador"""
    agent_name: str
    confidence: float
    reasoning: str

class FAQDocument(BaseModel):
    """Documento da FAQ"""
    id: str
    title: str
    content: str
    url: Optional[str] = None
    category: Optional[str] = None

class HealthCheck(BaseModel):
    """Resposta de health check"""
    status: str
    timestamp: datetime
    version: str
    dependencies: Dict[str, str]