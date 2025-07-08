import aiohttp
import asyncio
from typing import Dict, Any, Optional
from project.config.settings import settings
import json

class HuggingFaceClient:
    """Cliente para API do Hugging Face"""

    def __init__(self):
        self.api_key = settings.HUGGINGFACE_API_KEY
        self.model = settings.HUGGINGFACE_MODEL
        self.base_url = settings.HUGGINGFACE_BASE_URL

        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY não configurada")

    async def generate_text(
        self, 
        prompt: str, 
        max_length: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> str:
        """Gerar texto usando o modelo Llama"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": max_length,
                "temperature": temperature,
                "top_p": top_p,
                "do_sample": True,
                "return_full_text": False
            }
        }

        url = f"{self.base_url}/models/{self.model}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        if isinstance(result, list) and len(result) > 0:
                            return result[0].get("generated_text", "")
                        return ""
                    else:
                        error_text = await response.text()
                        raise Exception(f"Erro da API Hugging Face: {response.status} - {error_text}")
            except asyncio.TimeoutError:
                raise Exception("Timeout na requisição para Hugging Face")
            except Exception as e:
                raise Exception(f"Erro ao conectar com Hugging Face: {str(e)}")

    async def health_check(self) -> bool:
        """Verificar se a API está funcionando"""
        try:
            result = await self.generate_text("Hello", max_length=10)
            return len(result) > 0
        except:
            return False

# Instância global do cliente
hf_client = HuggingFaceClient()