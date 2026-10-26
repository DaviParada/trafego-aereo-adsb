"""
Configuração central do coletor de tráfego aéreo.
Toda decisão de projeto mora aqui - o resto do código consome.
"""

from pathlib import Path

# --- Endereços da API ---
URL_STATES = "https://opensky-network.org/api/states/all"
URL_TOKEN = ("https://auth.opensky-network.org/auth/realms/"
    "opensky-network/protocol/openid-connect/token")

# --- Recorte geográfico ---
# Corredor São Paulo - Rio de Janeiro, com Vale do Paraíba no centro
# Área: 2.0° x 4.1° = 8.2 graus² -> faixa de 1 crédito por consulta.
CAIXA = {
    "lamin": -24.2,
    "lomin": -47.3,
    "lamax": -22.2,
    "lomax": -43.2,
    "extended": 1,
}

#--- Ritmo da coleta ---
INTERVALO_SEGUNDOS = 60
TIMEOUT_SEGUNDOS = 30

#--- Disco --
PASTA_DADOS = Path(__file__).parent / "dados"

# --- Esquema da resposta ---
# ORDEM EXATA dos campos como a API devolve. Não reordene.
COLUNAS_API = [
    "icao24",
    "callsign",
    "origin_country",
    "time_position",
    "last_contact",
    "longitude",
    "latitude",
    "baro_altitude",
    "on_ground",
    "velocity",
    "true_track",
    "vertical_rate",
    "sensors",
    "geo_altitude",
    "squawk",
    "spi",
    "position_source",
    "category",
]

# 'sensors' vem sempre nulo quando não filtramos por receptor.
COLUNAS_DESCARTADAS = {"sensors"}

# Cabeçalho do CSV: dois campos nossos + os campos úteis da API.
COLUNAS_CSV = ["ts_consulta", "time_servidor"] + [
    c for c in COLUNAS_API if c not in COLUNAS_DESCARTADAS
]