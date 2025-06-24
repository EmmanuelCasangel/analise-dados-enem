# Dashboard ENEM 📊

Este projeto apresenta um dashboard interativo para análise dos microdados do ENEM, utilizando [Streamlit](https://streamlit.io/). O objetivo é facilitar a visualização e compreensão dos dados educacionais oficiais disponibilizados pelo INEP.

## Funcionalidades

- **Introdução:** Contextualização sobre o ENEM e os bancos de dados utilizados.
- **Microdados ENEM 2023:** Análise dos dados individuais dos participantes do exame de 2023.
- **Microdados por Escola:** Visualização de indicadores agregados por instituição de ensino (2005-2015).

## Principais Fontes de Dados

1. **Microdados ENEM 2023**
   - Dados anonimizados dos participantes
   - Informações socioeconômicas e desempenho nas provas
   - Variáveis: notas por área, redação, demografia, tipo de escola, questionário socioeconômico

2. **Microdados ENEM por Escola**
   - Indicadores agregados por escola (2005-2015)
   - Médias de desempenho, INSE, taxas de participação e rendimento

## Como executar

1. Instale as dependências:
   ```bash
   pip install streamlit
   ```

2. Execute o dashboard:
   ```bash
   streamlit run main.py
   ```

3. Acesse no navegador o endereço exibido no terminal (geralmente http://localhost:8501).

## Observações

- Os dados utilizados são públicos e seguem as diretrizes da LGPD.
- Informações identificáveis foram removidas para preservar a privacidade dos participantes.

---

Projeto desenvolvido para análise exploratória dos dados do