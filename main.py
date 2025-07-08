# /main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Importa as configurações e os roteadores dos endpoints
from api.endpoints import chat #, knowledge_base
from config.settings import settings # Supõe um arquivo de configurações
#from services.knowledge_base_manager import initialize_knowledge_base # Função para carregar modelos/dados

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação para carregar recursos na inicialização
    e liberá-los no desligamento. É a forma moderna de lidar com eventos de startup/shutdown.
    """
    print("INFO:     Iniciando a aplicação...")
    # Tarefa de inicialização: carregar a base de conhecimento, modelos de embedding, etc.
    # Isso evita o carregamento a cada requisição, otimizando a performance.
    #await initialize_knowledge_base()
    print("INFO:     Aplicação iniciada e recursos carregados.")
    yield
    # Tarefas de desligamento (se necessário)
    print("INFO:     Encerrando a aplicação...")

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="AI Multi-Agent System",
    description="API para o sistema multi-agentes.",
    version="1.0.0",
    lifespan=lifespan  # Associa o gerenciador de ciclo de vida
)

# Endpoint global para verificação de saúde (health check)
@app.get("/health", tags=["Monitoring"])
async def health_check():
    """Verifica se a API está online e operacional."""
    return {"status": "ok", "message": "Service is running"}

# Inclui os roteadores dos diferentes módulos da API
# Cada roteador agrupa endpoints relacionados sob um prefixo comum.
api_prefix = f"/api/{settings.API_VERSION}"

app.include_router(chat.router, prefix=api_prefix, tags=["Chat"])
#app.include_router(knowledge_base.router, prefix=f"{api_prefix}/knowledge-base", tags=["Knowledge Base"])

# Exemplo de como adicionar outros roteadores
# from api.endpoints import agents_router
# app.include_router(agents_router, prefix=f"{api_prefix}/agents", tags=["Agents"])

print(f"INFO:     Documentação da API disponível em: http://{settings.API_HOST}:{settings.API_PORT}/docs")
