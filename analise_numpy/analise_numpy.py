from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURAÇÃO
# ============================================================

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_BASE = RAIZ_PROJETO / "dados" / \
    "Massa_Dados_Transporte_Autonomo_Cidade_Alfa_Tratada.xlsx"
CAMINHO_SAIDA = RAIZ_PROJETO / "dados" / \
    "Massa_Dados_Transporte_Autonomo_Analise_NumPy.xlsx"


# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

df = pd.read_excel(CAMINHO_BASE, sheet_name="Sheet1")

print("=" * 70)
print("ANÁLISE NUMPY - SMART TRANSPORT MONITOR")
print("=" * 70)


# ============================================================
# CONVERSÃO PARA ARRAYS NUMPY
# ============================================================

atraso = df["Atraso_Minutos"].to_numpy(dtype=float)
consumo = df["Consumo_Bateria_kWh"].to_numpy(dtype=float)
velocidade = df["Velocidade_Media_kmh"].to_numpy(dtype=float)
passageiros = df["Passageiros_Transportados"].to_numpy(dtype=float)
intervencoes = df["Intervencoes_Humanas"].to_numpy(dtype=float)
nivel_autonomia = df["Nivel_Autonomia"].to_numpy()
id_onibus_array = df["ID_Onibus"].to_numpy()


# ============================================================
# 1. AUDITORIA DA QUALIDADE DOS DADOS
# ============================================================

print("\n[1] AUDITORIA DA BASE")
print(f"Registros: {len(df)}")
print(f"Colunas: {df.shape[1]}")
print(f"Valores ausentes: {df.isna().sum().sum()}")
print(f"Registros duplicados: {df.duplicated().sum()}")
print(f"Ônibus monitorados: {df['ID_Onibus'].nunique()}")
print(f"Linhas monitoradas: {df['Linha'].nunique()}")
print(f"Datas analisadas: {df['Data'].nunique()}")


# ============================================================
# 2. ESTATÍSTICA DESCRITIVA
# ============================================================

print("\n[2] ESTATÍSTICA DESCRITIVA")

print("\nATRASOS")
print(f"Média: {np.mean(atraso):.2f} min")
print(f"Mediana: {np.median(atraso):.2f} min")
print(f"Desvio padrão: {np.std(atraso, ddof=1):.2f} min")
print(f"Mínimo: {np.min(atraso):.2f} min")
print(f"Máximo: {np.max(atraso):.2f} min")

print("\nCONSUMO DE BATERIA")
print(f"Média: {np.mean(consumo):.2f} kWh")
print(f"Mediana: {np.median(consumo):.2f} kWh")
print(f"Desvio padrão: {np.std(consumo, ddof=1):.2f} kWh")
print(f"Mínimo: {np.min(consumo):.2f} kWh")
print(f"Máximo: {np.max(consumo):.2f} kWh")


# ============================================================
# 3. AUTONOMIA E EFICIÊNCIA OPERACIONAL
# ============================================================

print("\n[3] AUTONOMIA E EFICIÊNCIA OPERACIONAL")

mascara_total = nivel_autonomia == "L4 Total"
mascara_parcial = nivel_autonomia == "L4 Parcial (Intervenção Humana)"

atraso_total = atraso[mascara_total]
atraso_parcial = atraso[mascara_parcial]

media_total = np.mean(atraso_total)
media_parcial = np.mean(atraso_parcial)
diferenca_media = media_parcial - media_total

pct_total_5 = np.mean(atraso_total > 5) * 100
pct_parcial_5 = np.mean(atraso_parcial > 5) * 100

print(f"Atraso médio - L4 Total: {media_total:.2f} min")
print(f"Atraso médio - L4 Parcial: {media_parcial:.2f} min")
print(f"Diferença média: {diferenca_media:.2f} min")
print(f"L4 Total com atraso > 5 min: {pct_total_5:.1f}%")
print(f"L4 Parcial com atraso > 5 min: {pct_parcial_5:.1f}%")


# ============================================================
# 4. BOOTSTRAP - INTERVALO DE CONFIANÇA
# ============================================================

print("\n[4] BOOTSTRAP DA DIFERENÇA DOS ATRASOS")

rng = np.random.default_rng(42)
n_bootstrap = 10000
diferencas_bootstrap = np.empty(n_bootstrap)

for i in range(n_bootstrap):
    amostra_parcial = rng.choice(
        atraso_parcial, size=len(atraso_parcial), replace=True)
    amostra_total = rng.choice(
        atraso_total, size=len(atraso_total), replace=True)
    diferencas_bootstrap[i] = np.mean(amostra_parcial) - np.mean(amostra_total)

limite_inferior, limite_superior = np.percentile(
    diferencas_bootstrap, [2.5, 97.5])

print(
    f"IC 95% da diferença média: {limite_inferior:.2f} a {limite_superior:.2f} minutos")


# ============================================================
# 5. TESTE DE PERMUTAÇÃO
# ============================================================

print("\n[5] TESTE DE PERMUTAÇÃO")

diferenca_observada = np.mean(atraso_parcial) - np.mean(atraso_total)
atrasos_combinados = np.concatenate((atraso_parcial, atraso_total))

n_parcial = len(atraso_parcial)
n_permutacoes = 20000
diferencas_permutadas = np.empty(n_permutacoes)

for i in range(n_permutacoes):
    dados_permutados = rng.permutation(atrasos_combinados)
    grupo_parcial_perm = dados_permutados[:n_parcial]
    grupo_total_perm = dados_permutados[n_parcial:]
    diferencas_permutadas[i] = np.mean(
        grupo_parcial_perm) - np.mean(grupo_total_perm)

p_valor = (np.sum(np.abs(diferencas_permutadas) >= abs(
    diferenca_observada)) + 1) / (n_permutacoes + 1)

print(f"Diferença observada: {diferenca_observada:.2f} min")
print(f"p-valor aproximado: {p_valor:.6f}")


# ============================================================
# 6. CORRELAÇÕES ENTRE VARIÁVEIS
# ============================================================

print("\n[6] CORRELAÇÕES ENTRE VARIÁVEIS")

nomes_variaveis = ["Intervenções", "Velocidade",
                   "Passageiros", "Consumo", "Atraso"]
dados_numericos = np.column_stack(
    (intervencoes, velocidade, passageiros, consumo, atraso))
matriz_correlacao = np.corrcoef(dados_numericos, rowvar=False)

print("\nMatriz de correlação:")
print(np.round(matriz_correlacao, 3))

for i, nome in enumerate(nomes_variaveis):
    print(f"{i}: {nome}")

print(f"\nIntervenções x atraso: {matriz_correlacao[0, 4]:.3f}")
print(f"Velocidade x consumo: {matriz_correlacao[1, 3]:.3f}")
print(f"Passageiros x consumo: {matriz_correlacao[2, 3]:.3f}")


# ============================================================
# 7. MODELO DE CONSUMO ENERGÉTICO
# ============================================================

print("\n[7] MODELO DE CONSUMO ENERGÉTICO")

X = np.column_stack((np.ones(len(df)), velocidade, passageiros))
coeficientes, _, _, _ = np.linalg.lstsq(X, consumo, rcond=None)

intercepto = coeficientes[0]
coef_velocidade = coeficientes[1]
coef_passageiros = coeficientes[2]

consumo_estimado = X @ coeficientes
residuos = consumo - consumo_estimado

ss_residuos = np.sum(residuos ** 2)
ss_total = np.sum((consumo - np.mean(consumo)) ** 2)
r_quadrado = 1 - (ss_residuos / ss_total)

print(f"Intercepto: {intercepto:.4f}")
print(f"Coef. velocidade: {coef_velocidade:.4f}")
print(f"Coef. passageiros: {coef_passageiros:.4f}")
print(f"R²: {r_quadrado:.4f}")


# ============================================================
# 8. DETECÇÃO DE CONSUMO ACIMA DO ESPERADO
# ============================================================

print("\n[8] DETECÇÃO DE VIAGENS COM CONSUMO ACIMA DO ESPERADO")

limite_residuo = np.percentile(residuos, 95)
consumo_acima_esperado = residuos > limite_residuo

df["Consumo_Esperado_kWh"] = consumo_estimado
df["Desvio_Consumo_kWh"] = residuos
df["Consumo_Acima_Esperado"] = consumo_acima_esperado

anomalias = df[df["Consumo_Acima_Esperado"]].copy()
anomalias = anomalias.sort_values("Desvio_Consumo_kWh", ascending=False)

print(f"Limite do percentil 95 dos resíduos: {limite_residuo:.2f} kWh")
print(f"Viagens identificadas: {len(anomalias)}")

print("\nTOP 10 VIAGENS COM MAIOR CONSUMO ACIMA DO ESPERADO:")
print(anomalias[
    ["ID_Viagem", "ID_Onibus", "Linha", "Velocidade_Media_kmh", "Passageiros_Transportados",
     "Consumo_Bateria_kWh", "Consumo_Esperado_kWh", "Desvio_Consumo_kWh"]
].head(10).to_string(index=False))


# ============================================================
# 9. ANÁLISE DE DESEMPENHO POR ÔNIBUS
# ============================================================

print("\n[9] ANÁLISE DE DESEMPENHO POR ÔNIBUS")

ids_onibus = np.sort(df["ID_Onibus"].unique())
resultados_onibus = []

for onibus in ids_onibus:
    mascara_onibus = id_onibus_array == onibus

    n_viagens = np.sum(mascara_onibus)
    atraso_medio = np.mean(atraso[mascara_onibus])
    percentual_intervencao = np.mean(intervencoes[mascara_onibus] > 0) * 100

    consumo_medio = np.mean(consumo[mascara_onibus])
    consumo_esperado_medio = np.mean(consumo_estimado[mascara_onibus])
    desvio_medio_consumo = np.mean(residuos[mascara_onibus])

    quantidade_anomalias = np.sum(consumo_acima_esperado[mascara_onibus])
    taxa_anomalias = np.mean(consumo_acima_esperado[mascara_onibus]) * 100

    resultados_onibus.append([
        onibus, n_viagens, atraso_medio, percentual_intervencao,
        consumo_medio, consumo_esperado_medio, desvio_medio_consumo,
        quantidade_anomalias, taxa_anomalias
    ])

df_onibus = pd.DataFrame(resultados_onibus, columns=[
    "ID_Onibus", "Total_Viagens", "Atraso_Medio_Min",
    "Percentual_Com_Intervencao", "Consumo_Medio_kWh",
    "Consumo_Esperado_Medio_kWh", "Desvio_Medio_Consumo_kWh",
    "Quantidade_Anomalias", "Taxa_Anomalias_Pct"
])

df_onibus = df_onibus.sort_values("Taxa_Anomalias_Pct", ascending=False)

print("\nDESEMPENHO DA FROTA:")
print(df_onibus.round(2).to_string(index=False))


# ============================================================
# 10. VEÍCULOS PRIORITÁRIOS PARA INVESTIGAÇÃO
# ============================================================

print("\n[10] VEÍCULOS PRIORITÁRIOS PARA INVESTIGAÇÃO")

media_atraso_frota = np.mean(atraso)
taxa_referencia_anomalias = 5.0

prioritarios = df_onibus[
    (df_onibus["Atraso_Medio_Min"] > media_atraso_frota) &
    (df_onibus["Taxa_Anomalias_Pct"] > taxa_referencia_anomalias)
]

print(f"Média geral de atraso da frota: {media_atraso_frota:.2f} min")
print(f"Taxa de referência de anomalias: {taxa_referencia_anomalias:.1f}%")

print("\nVEÍCULOS COM ATENÇÃO OPERACIONAL E ENERGÉTICA:")
print(prioritarios[
    ["ID_Onibus", "Atraso_Medio_Min",
        "Percentual_Com_Intervencao", "Taxa_Anomalias_Pct"]
].round(2).to_string(index=False))


# ============================================================
# 11. EXPORTAÇÃO DOS RESULTADOS
# ============================================================

print("\n[11] EXPORTAÇÃO DOS RESULTADOS")

with pd.ExcelWriter(CAMINHO_SAIDA) as writer:
    df.to_excel(writer, sheet_name="Viagens_Analisadas", index=False)
    df_onibus.to_excel(writer, sheet_name="Resumo_Onibus", index=False)
    anomalias.to_excel(writer, sheet_name="Anomalias_Energeticas", index=False)

print(f"Arquivo enriquecido salvo em: {CAMINHO_SAIDA}")
