import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from typing import List, Optional, Dict, Any
import os
from config.settings import settings 

class VectorStoreManager:
    """Gerencia o banco vetorial usando ChromaDB"""
    
    def __init__(self, embeddings_manager, persist_directory: str = settings.CHROMA_PERSIST_DIRECTORY):
        self.embeddings_manager = embeddings_manager
        self.persist_directory = persist_directory
        self.collection_name = settings.CHROMA_COLLECTION_NAME
        self.vector_store = None
        
        # Cria diretório se não existir
        os.makedirs(persist_directory, exist_ok=True)
    
    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """Cria banco vetorial a partir dos documentos"""
        try:
            print(f"Criando banco vetorial com {len(documents)} documentos...")
            
            self.vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings_manager.get_embeddings(),
                persist_directory=self.persist_directory,
                collection_name=self.collection_name
            )
            
            # Persiste o banco
            self.vector_store.persist()
            print("Banco vetorial criado e persistido com sucesso!")
            
            return self.vector_store
            
        except Exception as e:
            raise Exception(f"Erro ao criar banco vetorial: {str(e)}")
    
    def load_vector_store(self) -> Optional[Chroma]:
        """Carrega banco vetorial existente"""
        try:
            if os.path.exists(self.persist_directory):
                self.vector_store = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings_manager.get_embeddings(),
                    collection_name=self.collection_name
                )
                print("Banco vetorial carregado com sucesso!")
                return self.vector_store
            else:
                print("Banco vetorial não encontrado.")
                return None
        except Exception as e:
            print(f"Erro ao carregar banco vetorial: {str(e)}")
            return None
    
    def search_similar_documents(self, query: str, k: int = 5) -> List[Document]:
        """Busca documentos similares à consulta"""
        if not self.vector_store:
            raise Exception("Banco vetorial não inicializado")
        
        try:
            results = self.vector_store.similarity_search(query, k=k)
            return results
        except Exception as e:
            raise Exception(f"Erro na busca: {str(e)}")
    
    def search_with_scores(self, query: str, k: int = 5) -> List[tuple]:
        """Busca documentos com scores de similaridade"""
        if not self.vector_store:
            raise Exception("Banco vetorial não inicializado")
        
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return results
        except Exception as e:
            raise Exception(f"Erro na busca com scores: {str(e)}")
    
    def get_retriever(self, search_type: str = "similarity", k: int = 5):
        """Retorna retriever configurado"""
        if not self.vector_store:
            raise Exception("Banco vetorial não inicializado")
        
        return self.vector_store.as_retriever(
            search_type=search_type,
            search_kwargs={"k": k}
        )
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas da coleção"""
        if not self.vector_store:
            return {"error": "Banco vetorial não inicializado"}
        
        try:
            # Acessa a coleção diretamente
            collection = self.vector_store._collection
            count = collection.count()
            
            return {
                "total_documents": count,
                "collection_name": self.collection_name,
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            return {"error": str(e)}
