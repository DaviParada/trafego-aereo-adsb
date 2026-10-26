import requests
import config
import credenciais

# --- 1: Trocando as credenciais por um TOKEN ---
resposta_token = requests.post(
    config.URL_TOKEN,
    data = {
        "grant_type": "client_credentials",
        "client_id": credenciais.CLIENT_ID,
        "client_secret": credenciais.CLIENT_SECRET,
    },
    timeout = config.TIMEOUT_SEGUNDOS,
)

print("Status do token:", resposta_token.status_code)
resposta_token.raise_for_status()

token = resposta_token.json()["access_token"]

print("Token recebido:", len(token), "caracteres")


# --- 2: Usar o token para consultar a API ---
cabecalho = {"Authorization": f"Bearer {token}"}

resposta = requests.get(
    config.URL_STATES,
    params = config.CAIXA,
    headers = cabecalho,
    timeout = config.TIMEOUT_SEGUNDOS,
)

print("Status da consulta:", resposta.status_code)
print("Creditos restantes:", resposta.headers.get("X-Rate-Limit-Remaining"))

dados = resposta.json()
aeronaves = dados.get("states") or []

print("Aeronaves na caixa:", len(aeronaves))