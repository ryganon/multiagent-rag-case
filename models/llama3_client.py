import requests
import time
import json
import os
from huggingface_hub import InferenceClient
from huggingface_hub import login

from typing import Dict, Any, Optional
from config.settings import settings 

class Llama3Client:
    """Cliente para comunicação com o modelo LLAMA3 via API HuggingFace"""
    
    def __init__(self):
        self.api_key = settings.HUGGINGFACE_API_KEY        
        self.model_client = InferenceClient(model= "meta-llama/Llama-3.3-70B-Instruct")
        
        login(token=os.getenv("HF_TOKEN"))        
        
    def _make_request(self, prompt: str) -> str:
        """Faz requisição para a API com retry automático"""
                
        try:            
            prompt_messages = [{"role": "user", "content": prompt}]
            response = self.model_client.chat_completion(prompt_messages, max_tokens=50, temperature=0.01, logprobs=True, stream=False)

            print("INFO:     Response", str(response.choices[0].message))
            return(str(response.choices[0].message))
        
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão: {e}")
            
        return "Falha na comunicação após múltiplas tentativas"
    
    
    def test_connection(self) -> bool:
        """Testa a conexão com a API"""
        test_response = ""
        return "Erro" not in test_response and test_response != "Não foi possível gerar uma resposta"
