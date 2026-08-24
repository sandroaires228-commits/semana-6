# testador_api.py
import requests
from typing import List, Dict, Union

URL_API_GASTOS: str = "http://127.0.0.1:8000/api/gastos/"

def monitorar_geladeira_compras() -> None:
    """Consome a API de Finanças e audita os itens na geladeira de compras."""
    print("=== MONITOR DE ITENS E ATRITO COGNITIVO VIA API ===")

    try:
        # 1. Requisição GET com timeout de 5 segundos
        resposta = requests.get(URL_API_GASTOS, timeout=5)
        resposta.raise_for_status()

        # 2. Decodificação do JSON em Lista de Dicionários
        gastos: List[Dict[str, Union[int, str, float, bool]]] = resposta.json()

        print(f"Total de registros auditados: {len(gastos)}\n")
        print(f"{'ID':<5} | {'DESCRIÇÃO':<25} | {'VALOR (R$)':<12} | {'ESTADO':<15}")
        print("-" * 65)

        for g in gastos:
            print(f"#{g['id']:<4} | {g['descricao']:<25} | R$ {g['valor']:<9} | {g['estado']:<15}")

    except requests.exceptions.ConnectionError:
        print("Erro de Conexão: Não foi possível conectar à API do Django.")
        print("Certifique-se de que o servidor está rodando em 'http://127.0.0.1:8000/'.")
    except requests.exceptions.Timeout:
        print("Erro de Timeout: O tempo limite de rede expirou.")
    except requests.exceptions.RequestException as erro:
        print(f"Erro ao consumir API: {erro}")

if __name__ == "__main__":
    monitorar_geladeira_compras()