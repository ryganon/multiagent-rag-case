from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from typing import List
import torch
from config.settings import settings

class PortugueseEmbeddingsManager:
    """Gerencia embeddings em português usando sentence-transformers"""
    
    def __init__(self, model_name: str = settings.EMBEDDING_MODEL):
        self.model_name = model_name
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Usando dispositivo: {self.device}")
        
        # Inicializa o modelo de embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': self.device},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Modelo sentence-transformer para testes
        self.sentence_model = SentenceTransformer(model_name, device=self.device)
    
    def get_embeddings(self):
        """Retorna instância do modelo de embeddings"""
        return self.embeddings
    
    def test_embedding(self, text: str = "Este é um teste de embedding em português"):
        """Testa o modelo de embedding"""
        try:
            # Testa com LangChain
            embedding_vector = self.embeddings.embed_query(text)
            
            # Testa com sentence-transformers
            st_embedding = self.sentence_model.encode([text])
            
            return {
                'success': True,
                'embedding_dimension': len(embedding_vector),
                'sample_values': embedding_vector[:5],
                'sentence_transformer_dimension': st_embedding.shape[1]
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calcula similaridade entre dois textos"""
        from sentence_transformers import util
        
        embeddings = self.sentence_model.encode([text1, text2])
        similarity = util.cos_sim(embeddings[0], embeddings[1])
        return float(similarity[0][0])
    
    def get_model_info(self) -> dict:
        """Retorna informações sobre o modelo"""
        return {
            'model_name': self.model_name,
            'device': self.device,
            'max_seq_length': getattr(self.sentence_model, 'max_seq_length', 'N/A'),
            'embedding_dimension': self.sentence_model.get_sentence_embedding_dimension()
        }
