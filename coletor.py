"""
Coletor de tráfego aéreo, usando a API do OpenSky Network.
Consultae a API a cada n segundos e grava um CSV por dia.
"""
import csv
import time
from datetime import datetime, timezone

import requests

import config
import credenciais

def agora_utc():
    """Instante atual, sempre em UTC"""
    return datetime.now(timezone.utc)

def obter_token():
    """Troca as credenciais por um token de acesso."""
    resposta = requests.post(
        config.URL_TOKEN,
        data = {
            "grant_type": "client_credentials",
            "client_id": credenciais.CLIENT_ID,
            "client_secret": credenciais.CLIENT_SECRET,
        },
        timeout = config.TIMEOUT_SEGUNDOS,
    )
    resposta.raise_for_status()
    return resposta.json()["access_token"]

def consultar(token):
    """Pede à API as aeronaves dentro da caixa"""
    cabecalho = {"Authorization": f"Bearer {token}"}
    return requests.get(
        config.URL_STATES,
        params = config.CAIXA,
        headers = cabecalho,
        timeout = config.TIMEOUT_SEGUNDOS,
    )

def gravar(aeronaves, time_servidor, ts_consulta):
    """Acrescenta as aeronaves ao CSV do dia"""
    config.PASTA_DADOS.mkdir(exist_ok=True)

    caminho = config.PASTA_DADOS / f"estados_{ts_consulta:%Y-%m-%d}.csv"
    arquivo_novo = not caminho.exists()

    with open(caminho, "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames = config.COLUNAS_CSV,
            extrasaction = "ignore"
        )
        if arquivo_novo:
            escritor.writeheader()

        for linha in aeronaves:
            registro = dict(zip(config.COLUNAS_API, linha))
            registro["ts_consulta"] = ts_consulta.isoformat()
            registro["time_servidor"] = time_servidor
            escritor.writerow(registro)


def main():
    print(f"Coletor iniciado - intervalo de {config.INTERVALO_SEGUNDOS}s")
    print("Ctrl+C para parar.\n")

    token = obter_token()
    ciclos = 0
    linhas = 0

    while True:
        inicio = time.monotonic()
        ts = agora_utc()
        hora = f"{ts:%H:%M:%S}"

        try:
            resposta = consultar(token)

            if resposta.status_code == 401:
                print(f"[{hora}] Token expirou.Obtendo novo token...")
                token = obter_token()
                resposta = consultar(token)

            if resposta.status_code == 429:
                print(f"[{hora}] Cota esgotada (429)." )
            elif resposta.status_code != 200:
                print(f"[{hora}] Resposta inesperada: {resposta.status_code}")
            else:
                dados = resposta.json()
                aeronaves = dados.get("states") or []
                gravar(aeronaves, dados.get("time"), ts)

                ciclos += 1
                linhas += len(aeronaves)
                creditos = resposta.headers.get("X-Rate-limit-Remaining")
                print(
                    f"[{hora}] {len(aeronaves):3d} aeronaves, |"
                    f"creditos {creditos} | ciclos {ciclos} | linhas {linhas}"                    
                )
        except requests.exceptions.RequestException as erro:
            print(f"[{hora}] Falha de rede: {erro}")

        except Exception as erro:
            print(f"[{hora}] Erro inesperado: {erro}")

        decorrido = time.monotonic() - inicio
        time.sleep(max(0, config.INTERVALO_SEGUNDOS - decorrido))

if __name__ == "__main__":
    main()





