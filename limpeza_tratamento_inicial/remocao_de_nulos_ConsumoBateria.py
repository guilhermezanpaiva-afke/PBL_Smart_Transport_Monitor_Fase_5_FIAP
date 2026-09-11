import pandas as pd

# 1. Carregamento dos dados
# Lê a aba 'Massa_de_Dados' da planilha Excel original do projeto
df = pd.read_excel(
    '../dados/Massa_Dados_Transporte_Autonomo_Cidade_Alfa_Tratada.xlsx',
    sheet_name='Massa_de_Dados',
)

# 2. Imputação estatística de valores ausentes (NaN)
# Calcula a mediana de consumo agrupada por 'Linha' e 'Turno' (viagens semelhantes)
mediana_grupo = df.groupby(['Linha', 'Turno'])[
    'Consumo_Bateria_kWh'
].transform('median')

# Preenche apenas as células nulas da coluna de consumo com a mediana do seu respectivo grupo
df['Consumo_Bateria_kWh'] = df['Consumo_Bateria_kWh'].fillna(mediana_grupo)

# 3. Exportação do dataset tratado
# Salva a base tratada de volta no Excel, preservando a aba e removendo a coluna de índice do Pandas
df.to_excel(
    'Massa_Dados_Transporte_Autonomo_Cidade_Alfa_Tratada.xlsx',
    sheet_name='Massa_de_Dados',
    index=False,
)
