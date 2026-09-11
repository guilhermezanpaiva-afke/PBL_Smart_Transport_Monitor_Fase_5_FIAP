import pandas as pd

# 1. Carregamento dos dados
# Lê o arquivo Excel com a massa de dados do transporte autônomo
df = pd.read_excel('Massa_Dados_Transporte_Autonomo_Cidade_Alfa_Tratada.xlsx')

# 2. Definição das colunas de texto para sanitização
# Lista as colunas categóricas que precisam de limpeza de espaços em branco
colunas_texto = ['Linha', 'Turno', 'Status_Sensores']

# 3. Limpeza e padronização das strings
# Converte os valores para texto (str) e remove espaços extras no início/fim (.strip())
for col in colunas_texto:
    df[col] = df[col].astype(str).str.strip()

# 4. Exportação do arquivo tratado
# Salva as alterações de volta no Excel sem incluir a coluna de índice do Pandas
df.to_excel(
    'Massa_Dados_Transporte_Autonomo_Cidade_Alfa_Tratada.xlsx', index=False
)
