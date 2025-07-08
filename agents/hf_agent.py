from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from models.llama3_client import Llama3Client
from typing import List, Dict, Any, Optional
from models.schemas import ChatResponse
from rag.rag_knowledge_base import KnowledgeBaseRAG

class HFAgent:
    """Agente especializado em pesquisa e análise usando LLAMA3"""
    
    def __init__(self):
        self.llama_client = Llama3Client()
        self.conversation_history: List[BaseMessage] = []
        self.rag_engine = KnowledgeBaseRAG()
        
        self.rag_engine.setup_knowledge_base()
        
    def _create_prompt(self, query: str, context: str = '') -> str:
        """Cria prompt otimizado para pesquisa"""
        
        research_prompt = f"""Você é um assistente especializado. Sua tarefa é fornecer informações precisas, detalhadas e bem estruturadas sobre o tópico solicitado.

Diretrizes:
- Você deve usar somente os dados enviados no contexto a seguir.
- Forneça informações factuais e precisas
- Estruture a resposta de forma clara e organizada
- Se não souber algo, indique claramente

Pergunta: {query}

Contexto: {context}

Resposta:"""
        
        return research_prompt

    def _query_knowledge_base(self, question: str) -> str:
        """Consulta a base de conhecimento"""
                
        result = self.rag_engine.query_knowledge_base(question)
        
        # usar primeiro resultado
        return result[0][0]['content']


    def _format_response(self, response: str) -> str:
        """Formata a resposta do modelo para melhor apresentação"""
        
        if not response:
            return "Não foi possível gerar uma resposta para sua consulta."
        
        # Remove possíveis artefatos do modelo
        response = response.strip()
        
        # Adiciona prefixo identificador
        formatted_response = f"**[Agente de Pesquisa]**\n\n{response}"
        
        return formatted_response
    
    async def process(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> ChatResponse:      
               
        try:        
            # Baseado na mensagem, executa RAG na base de conhecimento    
            context = self._query_knowledge_base(message)

            # Cria prompt especializado
            prompt = self._create_prompt(message, context)

            print(f"LLM:     PROMPT: {prompt}")
            
            # Obtém resposta do LLAMA3
            raw_response = self.llama_client._make_request(prompt)
            
            # Formata resposta
            formatted_response = self._format_response(raw_response)
            
            # Histórico de conversação do agente
            self.conversation_history.extend([
                HumanMessage(content=message),
                AIMessage(content=formatted_response)
            ])
            
            return ChatResponse(
                response=formatted_response,
                agent_used="llama3",
                session_id="request.session_id"
            )
                    
        except Exception as e:
            error_message = f"🔬 **[Agente de Pesquisa]**\n\nErro ao processar consulta: {str(e)}"
            return error_message
    
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Retorna histórico de conversação formatado"""
        
        history = []
        for message in self.conversation_history:
            if isinstance(message, HumanMessage):
                history.append({"role": "user", "content": message.content})
            elif isinstance(message, AIMessage):
                history.append({"role": "assistant", "content": message.content})
        
        return history
    
    def clear_history(self):
        """Limpa o histórico de conversação"""
        self.conversation_history.clear()
