import pandas as pd

# 1. Carregamento dos dados
# Lê a aba 'Massa_de_Dados' da planilha Excel no diretório indicado
df = pd.read_excel(
    '../dados/Massa_Dados_Transporte_Autonomo_Cidade_Alfa_Tratada.xlsx',
    sheet_name='Massa_de_Dados',
)

# 2. Tratamento de valores ausentes (NaN) em dados categóricos
# Substitui registros nulos na coluna 'Status_Sensores' pelo texto padrão 'Não Registrado'
df['Status_Sensores'] = df['Status_Sensores'].fillna(value='Não Registrado')

# 3. Exportação do dataset atualizado
# Grava as alterações na planilha Excel, mantendo o nome da aba e omitindo o índice
df.to_excel(
    'Massa_Dados_Transporte_Autonomo_Cidade_Alfa_Tratada.xlsx',
    sheet_name='Massa_de_Dados',
    index=False,
)
