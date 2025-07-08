import sys 
import os

# dentro de project -> python -m tests.rag tests/rag.py
from rag.rag_knowledge_base import KnowledgeBaseRAG


def main():
    rag_engine = KnowledgeBaseRAG()
    rag_engine.setup_knowledge_base()
    
    result = rag_engine.query_knowledge_base("Hotmart Journey")
    
    # Exibe fontes se disponíveis
    for i, doc in enumerate(result[0][:3], 1):
        print(f"  {i}. {doc['article_name']}")
        if doc.get('similarity_score'):
            print(f"     Similaridade: {doc['similarity_score']:.3f}")   

if __name__ == "__main__":
    main()