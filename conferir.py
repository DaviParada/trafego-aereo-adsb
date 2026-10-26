"""
Conferência do dado coletado. Só lê — não altera nada.
"""

import pandas as pd

import config

arquivos = sorted(config.PASTA_DADOS.glob("estados_*.csv"))
print(f"Arquivos: {len(arquivos)}")

df = pd.concat(
    (pd.read_csv(a, on_bad_lines="skip") for a in arquivos),
    ignore_index=True,
)
df["ts_consulta"] = pd.to_datetime(df["ts_consulta"])

print(f"Linhas: {len(df):,}")
print(f"Aeronaves distintas: {df['icao24'].nunique():,}")
print(f"De {df['ts_consulta'].min()} ate {df['ts_consulta'].max()}")

# --- Saúde da coleta ---
ciclos = df["ts_consulta"].drop_duplicates().sort_values()
intervalos = ciclos.diff().dt.total_seconds().dropna()
buracos = intervalos[intervalos > 120]

print(f"\nCiclos: {len(ciclos):,}")
print(f"Intervalo mediano: {intervalos.median():.0f} s")
print(f"Buracos acima de 2 min: {len(buracos)}")
if len(buracos):
    print(f"Maior buraco: {buracos.max() / 60:.1f} min")

# --- Preenchimento ---
print("\n% ausente por coluna:")
ausentes = df.isna().mean().mul(100).round(1)
print(ausentes[ausentes > 0].sort_values(ascending=False).to_string())

# --- Categoria ---
cs = df["callsign"].fillna("").str.strip()
print(f"\nCallsign de companhia: {cs.str.match(r'^[A-Z]{3}[0-9]').mean() * 100:.1f}%")
print(f"Callsign vazio: {(cs == '').mean() * 100:.1f}%")