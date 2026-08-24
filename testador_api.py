import requests
from typing import List, Dict, Union

URL_API_GASTOS: str = "http://127.0.0.1:8000/api/gastos/"

def listar_gastos_api() -> None:
    """Realiza uma requisição GET para auditar os lançamentos."""
    print("\n=== 1. AUDITORIA DE LANÇAMENTOS (GET) ===")
    try:
        resposta = requests.get(URL_API_GASTOS, timeout=5)
        resposta.raise_for_status()

        gastos: List[Dict[str, Union[int, str, float, bool]]] = resposta.json()

        print(f"Total de registros localizados: {len(gastos)}\n")
        print(f"{'ID':<5} | {'DESCRIÇÃO':<25} | {'VALOR (R$)':<12} | {'ESTADO':<15}")
        print("-" * 65)

        for g in gastos:
            print(f"#{g['id']:<4} | {g['descricao']:<25} | R$ {g['valor']:<9} | {g['estado']:<15}")

    except requests.exceptions.ConnectionError:
        print("Erro de Conexão: O servidor Django está desligado.")
    except requests.exceptions.RequestException as erro:
        print(f"Falha na requisição: {erro}")

def cadastrar_gasto_api(descricao: str, valor: float, impulso: bool) -> None:
    """Realiza uma requisição POST enviando payload JSON."""
    print(f"\n=== 2. INSERINDO ITEM VIA API (POST): {descricao} ===")
    
    payload = {
        "descricao": descricao,
        "valor": valor,
        "categoria": "eletronicos",
        "impulso": impulso
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    try:
        resposta = requests.post(URL_API_GASTOS, json=payload, headers=headers, timeout=5)
        resposta.raise_for_status()
        
        print(f"Resposta do Servidor: {resposta.json()}")
    except requests.exceptions.RequestException as erro:
        print(f"Erro ao inserir via POST: {erro}")

if __name__ == "__main__":
    # Teste 1: Cadastrar um item por impulso via API
    cadastrar_gasto_api("Smartband Fitness", 250.00, impulso=True)
    
    # Teste 2: Listar a tabela atualizada
    listar_gastos_api()