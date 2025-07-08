# Projeto: Sistema Multi-Agente com RAG e LLM

## Visão Geral

Este projeto implementa um sistema de atendimento automatizado baseado em múltiplos agentes, utilizando técnicas de RAG (Retrieval-Augmented Generation) e modelos de linguagem (LLM) para fornecer respostas precisas e contextualizadas a partir de uma base de conhecimento estruturada.

### Principais Features

- **Arquitetura Multi-Agente:** Agentes especializados para pesquisa, roteamento e interação.
- **RAG (Retrieval-Augmented Generation):** Busca semântica em base de conhecimento para enriquecer as respostas.
- **LLM (Llama3):** Integração com modelo de linguagem para geração de respostas detalhadas.
- **API REST:** Interface de comunicação via FastAPI.
- **Gerenciamento de Sessão:** Histórico de conversas e limpeza de sessão.
- **Configuração Modular:** Fácil expansão e manutenção.

---

## Estrutura de Pastas

```
project/
│
├── agents/                # Agentes especializados (ex: hf_agent.py)
├── api/                   # Endpoints da API (ex: endpoints/chat.py)
├── config/                # Configurações globais
├── models/                # Integração com LLM e schemas
├── rag/                   # Engine de RAG e base de conhecimento
├── data/                  # Base de conhecimento (ex: data.csv)
├── tests/                 # Testes automatizados
└── main.py                # Ponto de entrada do sistema
```

---

## Pré-requisitos

- Python 3.9+
- Token de conta da Huggingface para uso de modelos de LLM (LLAMA3).
- (Opcional) CUDA/cuDNN para aceleração via GPU na geraçãod e Emeddings.


---

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <nome_da_pasta>
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Pacotes utilizados:**
   - Ou com pip:
     ```bash
     fastapi
     uvicorn
     langchain
     openai
     pydantic
     httpx
     tqdm
     numpy
     scikit-learn
     pandas
     sentence-transformers
     huggingface-hub
     pytest
     ```

---

## Execução

1. **Configure variáveis de ambiente (se necessário):**
   - Exemplo: chaves de API, configurações de modelo, etc.
   - Veja o arquivo `config/settings.py` para detalhes.

2. **Inicie o sistema:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Acesse a API:**
   - Por padrão, estará disponível em: [http://localhost:8000](http://localhost:8000)
   
---

## Exemplos de Uso

**Teste com Endpoint de chat:**  
 ```
    project/
    ├── tests/     
        ├── message.py
 ```
```bash
python message.py   
```
---

## Observações

- A base de conhecimento deve estar em `data/data.csv`.
- O sistema utiliza embeddings em português para busca semântica.
- O modelo Llama3 é acessado via HuggingFace ou endpoint local, conforme configuração.

---

# Sobre o projeto

 A seguir, um descritivo das features implementadas.

### Arquitetura Multi-Agentes

O projeto utiliza múltiplos agentes especializados, cada um com responsabilidades distintas, como pesquisa (LLM), roteamento, interação humana e análise de jornadas.
O roteamento de mensagens é feito pelo RouterAgent, que decide qual agente deve processar cada mensagem.

### Sistema RAG (Retrieval-Augmented Generation)
Implementação de um sistema RAG para responder perguntas com base em uma base de conhecimento estruturada em CSV.
O core do sistema está na classe KnowledgeBaseRAG, que gerencia processamento de documentos, embeddings, armazenamento vetorial e integração com LLM.
Utiliza embeddings em português e armazenamento vetorial para busca semântica eficiente.

### Base de Conhecimento
Os dados são carregados de um arquivo CSV (data/data.csv), processados e indexados para busca.
O pipeline inclui processamento de documentos, geração de embeddings (PortugueseEmbeddingsManager), e armazenamento vetorial (VectorStoreManager).

### Integração com LLM (Llama3 via HuggingFace)
O agente HFAgent utiliza o modelo Llama3 para gerar respostas detalhadas, estruturando prompts com contexto recuperado da base de conhecimento.
O cliente para requisições ao modelo está em Llama3Client.

### API REST com FastAPI
A API principal está em main.py, utilizando FastAPI para expor endpoints.
Endpoint de chat em chat.py, que recebe mensagens do usuário e retorna respostas do sistema multi-agentes.
Endpoint de health check para monitoramento.

### Gerenciamento de Sessão e Histórico
Cada agente pode manter histórico de conversação, como visto em HFAgent.get_conversation_history.
Possibilidade de limpar histórico de sessão.

### Configuração e Modularidade
Configurações centralizadas em config/settings.py.
Estrutura modular para fácil expansão de agentes, ferramentas e integrações.

### Testes e Utilitários
Estrutura para testes automatizados em tests/.
Utilitários diversos em utils/.


# Pontos de Melhoria

## Funcionalidades ainda não implementadas
- Handoff para agente humano.
- Identificação de usuário na jornada Stars e Legacy.
- Criação de report sobre o ambiente em execução.

## Testes Automatizados e Integração

- **Cobertura de Testes:**  
  Ampliar a cobertura de testes unitários e de integração, incluindo casos de sucesso, falha e borda para todos os endpoints da API.
- **Testes de Integração de Ambientes:**  
  Implementar pipelines de CI/CD (ex: GitHub Actions, GitLab CI) para rodar testes automatizados em diferentes ambientes (desenvolvimento, homologação, produção).
- **Mock de Serviços Externos:**  
  Utilizar mocks para dependências externas (ex: LLM, base de conhecimento) nos testes, garantindo isolamento e reprodutibilidade.
- **Testes de Performance:**  
  Adicionar testes de carga e stress para avaliar a escalabilidade da API.

## Estrutura e Organização do Código

- **Padronização de Endpoints:**  
  Garantir que todos os endpoints sigam convenções REST e estejam bem documentados.
- **Documentação de Código:**  
  Melhorar docstrings e comentários, facilitando manutenção e onboarding de novos desenvolvedores.

## Segurança

- **Validação de Dados:**  
  Garantir validação rigorosa de entradas da API usando Pydantic ou outra biblioteca.
- **Autenticação e Autorização:**  
  Implementar mecanismos de autenticação (ex: OAuth2, JWT) e autorização para proteger endpoints sensíveis.

## Experiência do Usuário e API

- **Mensagens de Erro Amigáveis:**  
  Padronizar e detalhar mensagens de erro retornadas pela API.
- **Documentação Interativa:**  
  Manter e expandir a documentação interativa da API (Swagger/OpenAPI).
- **Versionamento da API:**  
  Garantir versionamento claro dos endpoints para facilitar evolução sem breaking changes.

## Escalabilidade e Performance

- **Cache de Respostas:**  
  Implementar cache para respostas frequentes, reduzindo latência e carga no LLM.
- **Gerenciamento de Sessão:**  
  Avaliar persistência de sessões em banco de dados para suportar múltiplos servidores.
- **Otimização de Consultas RAG:**  
  Melhorar performance das buscas na base de conhecimento, considerando indexação e paralelização.

