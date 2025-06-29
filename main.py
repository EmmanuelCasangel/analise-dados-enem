import pandas as pd
import streamlit as st
import numpy as np
import seaborn as sns
from scipy.stats import chi2_contingency
import os
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from kmodes.kmodes import KModes
import plotly.express as px
import os
import string

from sklearn.feature_selection import mutual_info_regression

from utils import traducoes_variaveis, valores_variaveis, calcular_pontuacao


def main():
    colunas_necessarias = [
        'TP_FAIXA_ETARIA', 'TP_SEXO', 'TP_ESTADO_CIVIL', 'TP_COR_RACA', 'TP_NACIONALIDADE',
        'TP_ST_CONCLUSAO', 'TP_ESCOLA', 'IN_TREINEIRO', 'TP_PRESENCA_CN',
        'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH',
        'NU_NOTA_LC', 'NU_NOTA_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2',
        'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO',
        'Q001', 'Q002', 'Q003', 'Q004', 'Q005', 'Q006', 'Q007', 'Q008', 'Q009', 'Q010',
        'Q011', 'Q012', 'Q013', 'Q014', 'Q015', 'Q016', 'Q017', 'Q018', 'Q019', 'Q020',
        'Q021', 'Q022', 'Q023', 'Q024', 'Q025'
    ]

    df = pd.read_csv(
        'dados_enem/microdados_enem_2023/DADOS/MICRODADOS_ENEM_2023.csv',
        sep=';',
        encoding='latin1',
        usecols=colunas_necessarias
    )


    st.set_page_config(
        page_title="Dashboard ENEM",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("Análise de Dados do ENEM")
    st.subheader("Dashboard de Microdados Educacionais")
    
    tab_intro, tab_enem2023, tab_clusterizacao, tab_conclusao, tab_exploracao = st.tabs([
        "Introdução", 
        "Microdados ENEM 2023",
        "Clusterização de Dados",
        "Conclusão",
        "Exploração de Dados",
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
        
        st.header("Objetivo do Dashboard")
        st.markdown("""
        Este dashboard tem como objetivo analisar quais parcelas da sociedade são efetivamente alcançadas pelo ENEM em relação ao acesso ao ensino superior. 
        Busca-se identificar e evidenciar possíveis vieses associados a fatores socioeconômicos, permitindo compreender de que forma as condições sociais dos participantes influenciam suas oportunidades de ingresso na universidade. 
        A análise visa contribuir para o debate sobre a equidade do exame e seu papel como instrumento de democratização do ensino superior no Brasil.
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

        st.info("""
        **Nota importante:** Os dados são oficiais do INEP e seguem as diretrizes da 
        Lei Geral de Proteção de Dados (LGPD). Informações identificáveis foram 
        removidas ou anonimizadas para preservar a privacidade dos participantes.
        """)

    with tab_enem2023:
        st.header("Análise dos Microdados ENEM 2023")
        st.markdown("""
        Nesta seção, serão apresentados gráficos e análises dos microdados do ENEM 2023,
        com foco em aspectos socioeconômicos, desempenho e características dos participantes.
        """)

        st.subheader("Distribuição de Situação por Tipo de Escola")



        # Cria uma coluna de status para cada linha (presente, ausente/eliminado)
        def classifica_status(row):
            if all(row[col] == 1 for col in ['TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT']):
                return 'Presente'
            elif any(row[col] == 0 or row[col] == 2 for col in
                     ['TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT']):
                return 'Ausente/Eliminado'
            return np.nan

        resultado_path = 'resultado_tipo_escola.csv'
        if os.path.exists(resultado_path):
            df_resultado = pd.read_csv(resultado_path)
        else:
            df['Status'] = df.apply(classifica_status, axis=1)

            # Mapeia os tipos de escola para nomes legíveis
            mapa_escola = {1: 'Pública', 2: 'Privada', 3: 'Não Informada'}
            df['Tipo de Escola'] = df['TP_ESCOLA'].map(mapa_escola)

            # Agrupa e conta
            agrupado = df.groupby(['Tipo de Escola', 'Status']).size().unstack(fill_value=0)
            agrupado['Total'] = agrupado.sum(axis=1)
            agrupado['% Presentes'] = agrupado.get('Presente', 0) / agrupado['Total'] * 100
            agrupado['% Ausentes/Eliminados'] = agrupado.get('Ausente/Eliminado', 0) / agrupado['Total'] * 100

            # Prepara DataFrame final
            df_resultado = agrupado.reset_index()[
                ['Tipo de Escola', '% Presentes', '% Ausentes/Eliminados', 'Presente', 'Ausente/Eliminado',
                 'Total']].fillna(0)
            df_resultado.to_csv(resultado_path, index=False)



        # Visualização
        st.subheader("Percentual e Total de Presença/Ausência por Tipo de Escola")
        st.dataframe(
            df_resultado[
                ["Tipo de Escola", "% Presentes", "% Ausentes/Eliminados", "Presente", "Ausente/Eliminado", "Total"]],
            use_container_width=True
        )
        st.bar_chart(
            df_resultado.set_index("Tipo de Escola")[["% Presentes", "% Ausentes/Eliminados"]],
            use_container_width=True
        )

    with tab_exploracao:
        def cramers_v(x, y):
            confusion_matrix = pd.crosstab(x, y)
            chi2 = chi2_contingency(confusion_matrix)[0]
            n = confusion_matrix.sum().sum()
            phi2 = chi2 / n
            r, k = confusion_matrix.shape
            phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
            rcorr = r - ((r - 1) ** 2) / (n - 1)
            kcorr = k - ((k - 1) ** 2) / (n - 1)
            return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))

        with tab_exploracao:
            st.header("Escolhendo variaveis categóricas mais interessantes para clusterizacão")

            st.markdown("""
                Nesta seção, buscamos identificar quais variáveis categóricas são mais relevantes para a clusterização em relação às notas do ENEM.

                O primeiro passo consiste em calcular a correlação entre as variáveis categóricas utilizando o V de Cramer, a fim de identificar possíveis redundâncias. Caso sejam encontradas variáveis altamente correlacionadas, podemos optar por eliminar algumas delas para evitar sobreposição de informações.

                Em seguida, aplicamos a análise de informação mútua para determinar quais variáveis categóricas apresentam maior relação com as notas do ENEM. Dessa forma, selecionamos as variáveis mais significativas para compor a clusterização.
            """)
            variaveis_cat = [
                'Q001', 'Q002', 'Q003', 'Q004', 'Q005', 'Q006', 'Q007', 'Q008', 'Q009', 'Q010',
                'Q011', 'Q012', 'Q013', 'Q014', 'Q015', 'Q016', 'Q017', 'Q018', 'Q019', 'Q020',
                'Q021', 'Q022', 'Q023', 'Q024', 'Q025', 'TP_FAIXA_ETARIA', 'TP_SEXO', 'TP_ESTADO_CIVIL',
                'TP_COR_RACA', 'TP_ESCOLA'
            ]

            if os.path.exists('matriz_v_cramer.csv'):
                matriz_v = pd.read_csv('matriz_v_cramer.csv', index_col=0)
            else:
                df_cat = df[variaveis_cat].dropna()
                matriz_v = pd.DataFrame(
                    np.zeros((len(variaveis_cat), len(variaveis_cat))),
                    columns=variaveis_cat, index=variaveis_cat
                )

                for i, var1 in enumerate(variaveis_cat):
                    for j, var2 in enumerate(variaveis_cat):
                        if i >= j:
                            matriz_v.iloc[i, j] = cramers_v(df_cat[var1], df_cat[var2])

                # Salvar matriz V de Cramer
                matriz_v.to_csv('matriz_v_cramer.csv')


            # Extrai pares únicos (sem diagonal e sem duplicatas)
            correlacoes = []
            for i in range(len(variaveis_cat)):
                for j in range(i):
                    correlacoes.append((
                        variaveis_cat[i],
                        variaveis_cat[j],
                        matriz_v.iloc[i, j]
                    ))

            # Ordena do maior para o menor
            correlacoes_ordenadas = sorted(correlacoes, key=lambda x: x[2], reverse=True)

            # Cria DataFrame para exibir
            df_correlacoes = pd.DataFrame(correlacoes_ordenadas, columns=['Variável 1', 'Variável 2', 'V de Cramer'])

            st.subheader("Lista de Correlações (V de Cramer) - Ordem Decrescente")
            st.dataframe(df_correlacoes, use_container_width=True)


        # Defina as variáveis
        notas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
        categoricas = [
            'Q001', 'Q002', 'Q003', 'Q004', 'Q005', 'Q006', 'Q007', 'Q008', 'Q009', 'Q010',
            'Q011', 'Q012', 'Q013', 'Q014', 'Q015', 'Q016', 'Q017', 'Q018', 'Q019', 'Q020',
            'Q021', 'Q022', 'Q023', 'Q024', 'Q025', 'TP_FAIXA_ETARIA', 'TP_SEXO', 'TP_ESTADO_CIVIL',
            'TP_COR_RACA', 'TP_ESCOLA'
        ]

        # Remova nulos
        df_mi = df[notas + categoricas].dropna()

        # Codifique as variáveis categóricas como números inteiros
        df_encoded = df_mi.copy()
        for col in categoricas:
            df_encoded[col] = df_encoded[col].astype("category").cat.codes

        # Lista para armazenar os rankings de cada nota
        mi_rankings = []

        # Calcule e exiba o ranking para cada nota
        for nota in notas:

            if os.path.exists(f'mi_ranking_{nota}.csv'):
                mi_ranking = pd.read_csv(f'mi_ranking_{nota}.csv', index_col=0)
            else:
                mi_scores = mutual_info_regression(
                    df_encoded[categoricas], df_encoded[nota], discrete_features=True, random_state=0
                )
                mi_ranking = pd.Series(mi_scores, index=categoricas).sort_values(ascending=False)
                # Salva o ranking em CSV
                mi_ranking.to_csv(f'mi_ranking_{nota}.csv')


            mi_rankings.append(mi_ranking)
            # Exibe no Streamlit
            st.subheader(f"Variáveis categóricas mais correlacionadas com {nota}")
            st.dataframe(mi_ranking.reset_index().rename(columns={'index': 'Variável', 0: 'Informação Mútua'}))

        # Concatena todos os rankings em um DataFrame
        mi_concat = pd.concat(mi_rankings, axis=1)
        mi_concat.columns = notas

        # Calcula a média das informações mútuas para cada variável
        mi_concat['Média Informação Mútua'] = mi_concat.mean(axis=1)

        # Ordena do maior para o menor
        mi_geral = mi_concat['Média Informação Mútua'].sort_values(ascending=False)

        # Exibe no Streamlit
        st.subheader("Ranking Geral das Variáveis Categóricas (Média das Notas)")
        st.dataframe(mi_geral.reset_index().rename(
            columns={'index': 'Variável', 'Média Informação Mútua': 'Média Informação Mútua'}))

        # Seleciona os nomes das 10 variáveis com maior média
        top_10_variaveis_categoricas = mi_geral.head(10).index.tolist()
        st.subheader("Top 10 variáveis categóricas mais relevantes")
        st.write(top_10_variaveis_categoricas)
        max_cardinalidade = df[top_10_variaveis_categoricas].nunique().max()
        st.write(f"Cardinalidade máxima das top 10 variáveis categóricas: {max_cardinalidade}")
        min_cardinalidade = df[top_10_variaveis_categoricas].nunique().min()
        st.write(f"Cardinalidade mínima das top 10 variáveis categóricas: {min_cardinalidade}")
        media_cardinalidade = df[top_10_variaveis_categoricas].nunique().mean()
        st.write(f"Cardinalidade média das top 10 variáveis categóricas: {media_cardinalidade:.2f}")

        # Seleção das variáveis
        variaveis_cluster = top_10_variaveis_categoricas



        # Frequency Encoding
        df_freq = df[variaveis_cluster].copy()
        for col in variaveis_cluster:
            freq = df_freq[col].value_counts(normalize=True)
            df_freq[col] = df_freq[col].map(freq)


        K = [2, 3, 4, 5, 6, 7, 8]
        custos_path = 'custos_kmodes.csv'
        if os.path.exists(custos_path):
            custos = pd.read_csv(custos_path)['custo'].tolist()
        else:
            # Lista para armazenar o custo de cada k
            custos = []

            for k in K:
                km = KModes(n_clusters=k, init='Huang', n_init=3, verbose=0, random_state=42)
                km.fit(df_freq)
                custos.append(km.cost_)
            pd.DataFrame({'k': list(K), 'custo': custos}).to_csv(custos_path, index=False)

        # Plota o gráfico do cotovelo no Streamlit
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(K, custos, marker='o')
        ax.set_xlabel('Número de clusters (k)')
        ax.set_ylabel('Custo (inércia)')
        ax.set_title('Método do Cotovelo para KModes')
        ax.set_xticks(list(K))
        ax.grid(True)
        st.pyplot(fig)

    # with tab_clusterizacao:
#         st.header("Clusterização de Dados")
#         st.markdown("""
#         Nesta seção, aplicaremos técnicas de clusterização nos dados do ENEM, utilizando as variáveis categóricas mais relevantes identificadas anteriormente e as notas dos participantes.
#         O objetivo é agrupar os participantes com base em características comuns, permitindo uma análise mais aprofundada dos grupos formados.
#         """)
#
#         clusters_path = 'clusters_kmodes.csv'
#         if os.path.exists(clusters_path):
#             clusters = pd.read_csv(clusters_path)['cluster'].values
#         else:
#             # Ajuste do KModes
#             km = KModes(n_clusters=5, init='Huang', n_init=5, verbose=1)
#             clusters = km.fit_predict(df_freq)
#             pd.DataFrame({'cluster': clusters}).to_csv(clusters_path, index=False)
#
#         # Adiciona o cluster ao DataFrame
#         df_sample['cluster'] = clusters
#
#         # Defina uma paleta de cores bem contrastantes (exemplo para até 5 clusters)
#         cores_clusters = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
#
#
#         # Exibe os primeiros resultados
#         st.write(df_sample.head())
#
#         # Calcula a pontuação socioeconômica para cada participante da amostra
#         df_sample['pontuacao_socioeconomica'] = df_sample.apply(
#             lambda row: calcular_pontuacao(row.to_dict()), axis=1
#         )
#
#         # Gráfico de distribuição da pontuação socioeconômica por cluster
#         st.subheader("Distribuição da Pontuação Socioeconômica por Cluster")
#         fig, ax = plt.subplots(figsize=(8, 4))
#         sns.boxplot(
#             data=df_sample,
#             x='cluster',
#             y='pontuacao_socioeconomica',
#             palette=cores_clusters,
#             ax=ax
#         )
#         ax.set_xlabel('Cluster')
#         ax.set_ylabel('Pontuação Socioeconômica (0-100)')
#         ax.set_title('Distribuição da Pontuação Socioeconômica por Cluster')
#         st.pyplot(fig)
#
#         # Seletor de variável categórica
#         variavel_escolhida = st.selectbox(
#             "Escolha uma variável para visualizar a distribuição dos clusters:",
#             list(traducoes_variaveis.keys()),
#             format_func=lambda x: traducoes_variaveis.get(x, x)
#         )
#
#         # Tradução dos valores da variável
#         valores_dict = valores_variaveis.get(variavel_escolhida, {})
#
#         # Mapeia os valores para rótulos legíveis
#         df_sample['valor_legivel'] = df_sample[variavel_escolhida].map(valores_dict)
#
# #       Agrupa por valor da variável e cluster, conta ocorrências
#         df_plot = df_sample.groupby(['valor_legivel', 'cluster']).size().reset_index(name='contagem')
#
#
#         # Descobre as categorias presentes e ordena alfabeticamente
#         categorias_ordenadas = sorted(df_sample[variavel_escolhida].dropna().unique(),
#                                       key=lambda x: list(string.ascii_uppercase).index(str(x)) if str(
#                                           x) in string.ascii_uppercase else 99)
#
#         # Mapeia para rótulos legíveis na ordem correta
#         valores_legiveis_ordenados = [valores_dict.get(cat, cat) for cat in categorias_ordenadas]
#
#         # Atualiza a ordem das categorias no DataFrame
#         df_plot['valor_legivel'] = pd.Categorical(df_plot['valor_legivel'], categories=valores_legiveis_ordenados,
#                                                   ordered=True)
#
#         # Calcula o total por categoria
#         totais = df_plot.groupby('valor_legivel')['contagem'].transform('sum')
#         # Calcula a proporção
#         df_plot['proporcao'] = df_plot['contagem'] / totais
#
#         # Gráfico de barras ordenado
#         fig1 = px.bar(
#             df_plot.sort_values('valor_legivel'),
#             x='valor_legivel',
#             y='contagem',
#             color='cluster',
#             barmode='group',
#             color_discrete_sequence =cores_clusters,
#             category_orders={'valor_legivel': valores_legiveis_ordenados},
#             title=f'Distribuição dos clusters para {traducoes_variaveis.get(variavel_escolhida, variavel_escolhida)} (contagem)'
#         )
#         st.plotly_chart(fig1, use_container_width=True)
#
#         # O mesmo para o gráfico de proporção
#         fig2 = px.bar(
#             df_plot.sort_values('valor_legivel'),
#             x='valor_legivel',
#             y='proporcao',
#             color='cluster',
#             barmode='stack',
#             color_discrete_sequence=cores_clusters,
#             category_orders={'valor_legivel': valores_legiveis_ordenados},
#             title=f'Proporção dos clusters para {traducoes_variaveis.get(variavel_escolhida, variavel_escolhida)}'
#         )
#         st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    main()