import os
import sys
from typing import Dict, Any, List
import json

from rag.document_processor import CSVDocumentProcessor
from rag.embeddings_manager import PortugueseEmbeddingsManager
from rag.vector_store import VectorStoreManager

class KnowledgeBaseRAG:
    """Sistema RAG principal para base de conhecimento"""
    
    def __init__(self):
        #self.csv_path = csv_path
        self.doc_processor = None
        self.embeddings_manager = None
        self.vector_store_manager = None
        self.rag_system = None        
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Inicializa todos os componentes do sistema"""
        try:            
            #self.doc_processor = CSVDocumentProcessor(self.csv_path)
            self.embeddings_manager = PortugueseEmbeddingsManager()            
            self.vector_store_manager = VectorStoreManager(self.embeddings_manager)            
            #self.rag_system = RAGSystem(self.vector_store_manager)
            
        except Exception as e:
            print(f"Erro na inicialização: {str(e)}")
            raise
    
    def setup_knowledge_base(self, force_rebuild: bool = False):
        """Configura a base de conhecimento"""
        try:
            # Verifica se já existe um banco vetorial
            if not force_rebuild and self.vector_store_manager.load_vector_store():                 
                print(f"INFO:     Base de conhecimento carregada.")            
                return True          
          
            
        except Exception as e:
            print(f"INFO:     Erro ao configurar base de conhecimento: {str(e)}")            
            return False
    
    def query_knowledge_base(self, question: str) -> Dict[str, Any]:
        """Consulta a base de conhecimento"""       
        
        #result = self.rag_system.query(question)

        docs = self.vector_store_manager.search_with_scores(question, k=5)                
                    
        source_documents = self._format_search_results(docs),
        
        return source_documents # type: ignore

    def _format_search_results(self, results: List[tuple]) -> List[Dict[str, Any]]:
        """Formata resultados de busca com scores"""
        formatted_results = []
        
        for doc, score in results:
            formatted_results.append({
                #"content": doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content,
                "content": doc.page_content,
                "article_name": doc.metadata.get("article_name", "N/A"),
                "article_url": doc.metadata.get("article_url", "N/A"),
                "similarity_score": float(score),
                "chunk_index": doc.metadata.get("chunk_index", 0)
            })
        
        return formatted_results
