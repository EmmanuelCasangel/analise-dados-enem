import pandas as pd

def limpar_enem_microdados(df: pd.DataFrame) -> pd.DataFrame:
    # Remove colunas desnecessárias (exemplo)
    colunas_remover = ['NU_INSCRICAO']
    df = df.drop(columns=[col for col in colunas_remover if col in df.columns], errors='ignore')

    colunas_analise = [
        'TP_FAIXA_ETARIA', 'TP_SEXO', 'TP_ESTADO_CIVIL', 'TP_COR_RACA',
        'TP_ST_CONCLUSAO', 'TP_ESCOLA', 'IN_TREINEIRO', 'TP_PRESENCA_CN',
        'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH',
        'NU_NOTA_LC', 'NU_NOTA_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2',
        'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO',
        'Q001', 'Q002', 'Q003', 'Q004', 'Q005', 'Q006', 'Q007', 'Q008', 'Q009', 'Q010',
        'Q011', 'Q012', 'Q013', 'Q014', 'Q015', 'Q016', 'Q017', 'Q018', 'Q019', 'Q020',
        'Q021', 'Q022', 'Q023', 'Q024', 'Q025'
    ]

    nulos = df[colunas_analise].isnull().sum()
    total_linhas = len(df)
    percentuais = (nulos / total_linhas * 100).round(2)

    print("Quantidade de valores nulos e percentual por coluna:")
    for coluna in colunas_analise:
        print(f"{coluna}: {nulos[coluna]} nulos ({percentuais[coluna]}%)")

    return df

def obtem_alunos_presentes(df: pd.DataFrame) -> pd.DataFrame:
    colunas_presenca = ['TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT']
    return df[df[colunas_presenca].eq(1).all(axis=1)]

def obtem_alunos_ausentes_ou_eliminados(df: pd.DataFrame) -> pd.DataFrame:
    colunas_presenca = ['TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT']
    cond_ausente = df[colunas_presenca].eq(0).any(axis=1)
    cond_eliminados = df[df[colunas_presenca].eq(2).any(axis=1)]
    return df[cond_ausente | cond_eliminados]


def obtem_alunos_escola_publica(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['TP_ESCOLA'] == 1]

def obtem_alunos_escola_privada(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['TP_ESCOLA'] == 2]

def obtem_alunos_escola_nao_informada(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['TP_ESCOLA'] == 3]