import requests

URL = "https://opensky-network.org/api/states/all"

# Caixa cobrindo SJC e o Vale do Paraíba
CAIXA = {
    "lamin": -24.2,   #latitude mínima (sul) - abaixo de SP
    "lomin": -47.3,   #longitude mínima (oeste) - pega Campinas e Guarulhos
    "lamax": -22.2,   #latitude máxima (norte)
    "lomax": -43.2,    #longitude máxima (leste) - chega no Rj
}

resposta = requests.get(URL, params=CAIXA, timeout=30)

print("Status HTTP:", resposta.status_code)
print("Créditos restantes:", resposta.headers.get("X-Rate-Limit-Remaining"))

dados = resposta.json()
aeronaves = dados.get("states") or []

print("Aeronaves na caixa:", len(aeronaves))
print()

for linha in aeronaves[:5]:
    icao24 = linha[0]
    callsign = (linha[1] or "").strip()
    pais = linha[2]
    lon = linha[5]
    lat = linha[6]
    altitude = linha[7]
    print(f"{icao24} | {callsign:8} | {pais:18} | lat {lat} lon {lon} | {altitude} m")