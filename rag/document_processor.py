import pandas as pd
from typing import List, Dict, Any
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.settings import settings 

class CSVDocumentProcessor:
    """Processa arquivo CSV e converte em documentos LangChain"""
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
    
    def load_csv_data(self) -> pd.DataFrame:
        """Carrega dados do CSV"""
        try:
            df = pd.read_csv(self.csv_path)
            required_columns = ['article_name', 'article_url', 'article_content']
            
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"CSV deve conter as colunas: {required_columns}")
            
            # Remove linhas com conteúdo vazio
            df = df.dropna(subset=['article_content'])
            df = df[df['article_content'].str.strip() != '']
            
            return df
        except Exception as e:
            raise Exception(f"Erro ao carregar CSV: {str(e)}")
    
    def create_documents(self) -> List[Document]:
        """Converte dados CSV em documentos LangChain"""
        df = self.load_csv_data()
        documents = []
        
        for index, row in df.iterrows():
            # Cria conteúdo principal combinando título e conteúdo
            main_content = f"Título: {row['article_name']}\n\nConteúdo: {row['article_content']}"
            
            # Divide o conteúdo em chunks se necessário
            chunks = self.text_splitter.split_text(main_content)
            
            for i, chunk in enumerate(chunks):
                # Metadados para cada chunk
                metadata = {
                    'article_name': row['article_name'],
                    'article_url': row['article_url'],
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    'source': 'knowledge_base_csv'
                }
                
                # Cria documento LangChain
                doc = Document(
                    page_content=chunk,
                    metadata=metadata
                )
                documents.append(doc)
        
        return documents
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas dos dados processados"""
        df = self.load_csv_data()
        documents = self.create_documents()
        
        return {
            'total_articles': len(df),
            'total_chunks': len(documents),
            'avg_content_length': df['article_content'].str.len().mean(),
            'articles_with_multiple_chunks': len([doc for doc in documents if doc.metadata['total_chunks'] > 1])
        }
