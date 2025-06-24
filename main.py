import streamlit as st

def main():
    st.set_page_config(
        page_title="Dashboard ENEM",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("Análise de Dados do ENEM")
    st.subheader("Dashboard de Microdados Educacionais")
    
    tab_intro, tab_enem2023, tab_enem_escola = st.tabs([
        "Introdução", 
        "Microdados ENEM 2023", 
        "Microdados por Escola"
    ])
    
    with tab_intro:
        # Contexto sobre o ENEM
        st.header("Sobre o ENEM")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Objetivos principais:**
            - Avaliar o desempenho ao final da educação básica
            - Facilitar acesso ao ensino superior
            - Desenvolver indicadores educacionais
            - Promover autoavaliação dos participantes
            """)
        
        with col2:
            st.markdown("""
            **Evolução recente:**
            - 2009: Reformulação metodológica
            - 2017: Mudança para provas em dois domingos
            - 2020: Primeira versão digital
            - 2023: Novo formato de cadernos de prova
            """)

        st.divider()
        
        st.header("Contextualização dos Bancos de Dados")
        st.markdown("""
        Este dashboard analisa dois conjuntos de dados oficiais do INEP sobre o Exame Nacional do Ensino Médio (ENEM):
        """)
        
        # Container para Microdados ENEM 2023
        with st.expander("### 1. Microdados ENEM 2023", expanded=True):
            st.markdown("""
            **Fonte:** Instituto Nacional de Estudos e Pesquisas Educacionais (INEP)  
            **Período:** Dados referentes ao exame de 2023  
            **Objetivo:** Fornecer dados individuais dos participantes do ENEM
            
            **Principais características:**
            - Dados anonimizados de participantes
            - Informações socioeconômicas detalhadas
            - Desempenho nas provas objetivas e redação
            - Metadados sobre itens das provas
            - Questionário socioeconômico completo
            
            **Variáveis relevantes:**
            - Notas por área de conhecimento (CN, CH, LC, MT)
            - Descritores da redação (5 competências)
            - Informações demográficas (gênero, raça, idade)
            - Tipo de escola e situação de conclusão do EM
            - Respostas ao questionário socioeconômico (Q001-Q025)
            
            **Limitações:**
            - Dados pessoais removidos por LGPD
            - Exclusão de variáveis identificadoras
            - Faixas etárias em vez de idade exata
            """)
        
        # Container para Microdados por Escola
        with st.expander("### 2. Microdados ENEM por Escola", expanded=True):
            st.markdown("""
            **Fonte:** Instituto Nacional de Estudos e Pesquisas Educacionais (INEP)  
            **Período:** Dados históricos de 2005 a 2015  
            **Objetivo:** Fornecer indicadores de desempenho por instituição de ensino
            
            **Principais características:**
            - Dados agregados por escola
            - Médias de desempenho por área
            - Indicadores educacionais complementares
            - Taxas de participação e rendimento
            - Informações cadastrais das escolas
            
            **Variáveis relevantes:**
            - Médias por área de conhecimento
            - Nota de redação
            - Indicador de Nível Socioeconômico (INSE)
            - Taxas de aprovação/reprovação
            - Porte da escola e dependência administrativa
            
            **Contexto histórico:**
            - Programa descontinuado em 2017
            - Críticas sobre uso para rankings escolares
            - Substituído pelo SAEB como indicador oficial
            """)
        

        st.info("""
        **Nota importante:** Os dados são oficiais do INEP e seguem as diretrizes da 
        Lei Geral de Proteção de Dados (LGPD). Informações identificáveis foram 
        removidas ou anonimizadas para preservar a privacidade dos participantes.
        """)

if __name__ == "__main__":
    main()