# Documentação da Base de Dados — Cidade Alfa

Documentação detalhada da estrutura, tipos de dados e tratamentos aplicados na planilha `Massa_Dados_Transporte_Autonomo_Cidade_Alfa_Tratada.xlsx` (aba `Massa_de_Dados`).

---

## Estrutura das Colunas

| Coluna | Tipo de Dado (Pandas) | Descrição |
| :--- | :--- | :--- | :--- |
| **Linha** | `str` | Identificador da rota do veículo |
| **Turno** | `str` | Período da operação (ex: Manhã, Tarde, Noite) |
| **Consumo_Bateria_kWh** | `float64` | Consumo de energia em kWh por viagem |
| **Status_Sensores** | `str` | Diagnóstico de telemetria do veículo |
| **Atraso_Minutos** | `datetime64[ns]` | Atraso calculado com base no horário previsto da viagem |

---

## Regras de Higienização e Qualidade de Dados

1. **Tratamento de Nulos Numéricos:**
   * Ausências em `Consumo_Bateria_kWh` são preenchidas utilizando a mediana dos dados agrupados por **Linha** e **Turno**, garantindo estimativas realistas para cada perfil de viagem.

2. **Tratamento de Nulos Categóricos:**
   * Valores ausentes na telemetria de `Status_Sensores` são explicitados como `'Não Registrado'`, evitando falhas em agrupamentos futuros.

3. **Sanitização de Strings:**
   * Aplicação do método `.strip()` em colunas de texto para eliminação de espaços em branco invisíveis no início/fim das palavras.

---

*FIAP - 2026*
