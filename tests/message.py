# test_api.py
import httpx
import asyncio

# URL base da sua API
BASE_URL = "http://localhost:8000/api/v1"

async def test_chat_endpoint():
    """Testa o endpoint de chat."""
    payload = {       
        "message": "O que é o Hotmart Journey?"
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/chat", json=payload)
            #response.raise_for_status()
            print("\n--- Chat Endpoint ---")
            #print(f"Status Code: {response.status_code}")
            #print(f"Response: {response.json()}")
            print(f"Response: {response.content}")
    except httpx.HTTPStatusError as e:
        print(f"Erro HTTP ao testar chat: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Erro de requisição ao testar chat: {e}")

async def main():
    """Função principal para executar os testes."""    
    await test_chat_endpoint()

if __name__ == "__main__":
    asyncio.run(main())
