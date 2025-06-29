import pandas as pd

# def limpar_enem_microdados(df: pd.DataFrame) -> pd.DataFrame:
#     # Remove colunas desnecessárias (exemplo)
#     colunas_remover = ['NU_INSCRICAO']
#     df = df.drop(columns=[col for col in colunas_remover if col in df.columns], errors='ignore')
#
#     colunas_analise = [
#         'TP_FAIXA_ETARIA', 'TP_SEXO', 'TP_ESTADO_CIVIL', 'TP_COR_RACA',
#         'TP_ST_CONCLUSAO', 'TP_ESCOLA', 'IN_TREINEIRO', 'TP_PRESENCA_CN',
#         'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH',
#         'NU_NOTA_LC', 'NU_NOTA_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2',
#         'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO',
#         'Q001', 'Q002', 'Q003', 'Q004', 'Q005', 'Q006', 'Q007', 'Q008', 'Q009', 'Q010',
#         'Q011', 'Q012', 'Q013', 'Q014', 'Q015', 'Q016', 'Q017', 'Q018', 'Q019', 'Q020',
#         'Q021', 'Q022', 'Q023', 'Q024', 'Q025'
#     ]
#
#     nulos = df[colunas_analise].isnull().sum()
#     total_linhas = len(df)
#     percentuais = (nulos / total_linhas * 100).round(2)
#
#     print("Quantidade de valores nulos e percentual por coluna:")
#     for coluna in colunas_analise:
#         print(f"{coluna}: {nulos[coluna]} nulos ({percentuais[coluna]}%)")
#
#     return df

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


# Dicionário de traduções das variáveis do ENEM
traducoes_variaveis = {
    "Q001": "Até que série seu pai, ou o homem responsável por você, estudou?",
    "Q002": "Até que série sua mãe, ou a mulher responsável por você, estudou?",
    "Q003": "Ocupação do pai ou homem responsável",
    "Q004": "Ocupação da mãe ou mulher responsável",
    "Q005": "Quantidade de pessoas na residência",
    "Q006": "Renda mensal familiar",
    "Q007": "Empregado(a) doméstico(a) na residência",
    "Q008": "Possui banheiro na residência",
    "Q009": "Possui quartos para dormir",
    "Q010": "Possui carro",
    "Q011": "Possui motocicleta",
    "Q012": "Possui geladeira",
    "Q013": "Possui freezer",
    "Q014": "Possui máquina de lavar roupa",
    "Q015": "Possui máquina de secar roupa",
    "Q016": "Possui forno micro-ondas",
    "Q017": "Possui máquina de lavar louça",
    "Q018": "Possui aspirador de pó",
    "Q019": "Possui televisão em cores",
    "Q020": "Possui aparelho de DVD",
    "Q021": "Possui TV por assinatura",
    "Q022": "Possui telefone celular",
    "Q023": "Possui telefone fixo",
    "Q024": "Possui computador",
    "Q025": "Possui acesso à Internet",
    "TP_FAIXA_ETARIA": "Faixa etária",
    "TP_SEXO": "Sexo",
    "TP_ESTADO_CIVIL": "Estado civil",
    "TP_COR_RACA": "Cor/Raça",
    "TP_ESCOLA": "Tipo de escola",


}

# Dicionários para cada variável do questionário socioeconômico
valores_Q001 = {
    "A": "Nunca estudou.",
    "B": "Não completou a 4ª série/5º ano do Ensino Fundamental.",
    "C": "Completou a 4ª série/5º ano, mas não completou a 8ª série/9º ano do Ensino Fundamental.",
    "D": "Completou a 8ª série/9º ano do Ensino Fundamental, mas não completou o Ensino Médio.",
    "E": "Completou o Ensino Médio, mas não completou a Faculdade.",
    "F": "Completou a Faculdade, mas não completou a Pós-graduação.",
    "G": "Completou a Pós-graduação.",
    "H": "Não sei."
}

valores_Q002 = {
    "A": "Nunca estudou.",
    "B": "Não completou a 4ª série/5º ano do Ensino Fundamental.",
    "C": "Completou a 4ª série/5º ano, mas não completou a 8ª série/9º ano do Ensino Fundamental.",
    "D": "Completou a 8ª série/9º ano do Ensino Fundamental, mas não completou o Ensino Médio.",
    "E": "Completou o Ensino Médio, mas não completou a Faculdade.",
    "F": "Completou a Faculdade, mas não completou a Pós-graduação.",
    "G": "Completou a Pós-graduação.",
    "H": "Não sei."
}

valores_Q003 = {
    "A": "Grupo 1: Lavrador, agricultor sem empregados, bóia fria, criador de animais, etc.",
    "B": "Grupo 2: Diarista, empregado doméstico, motorista particular, vendedor, etc.",
    "C": "Grupo 3: Padeiro, sapateiro, torneiro mecânico, pedreiro, motorista, etc.",
    "D": "Grupo 4: Professor, técnico, policial, militar de baixa patente, etc.",
    "E": "Grupo 5: Médico, engenheiro, advogado, professor universitário, etc.",
    "F": "Não sei."
}

valores_Q004 = {
    "A": "Grupo 1: Lavradora, agricultora sem empregados, bóia fria, criadora de animais, etc.",
    "B": "Grupo 2: Diarista, empregada doméstica, motorista particular, vendedora, etc.",
    "C": "Grupo 3: Padeira, sapateira, torneira mecânica, pedreira, motorista, etc.",
    "D": "Grupo 4: Professora, técnica, policial, militar de baixa patente, etc.",
    "E": "Grupo 5: Médica, engenheira, advogada, professora universitária, etc.",
    "F": "Não sei."
}

valores_Q005 = {
    "1": "1, pois moro sozinho(a).",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "10": "10",
    "11": "11",
    "12": "12",
    "13": "13",
    "14": "14",
    "15": "15",
    "16": "16",
    "17": "17",
    "18": "18",
    "19": "19",
    "20": "20"
}

valores_Q006 = {
    "A": "Nenhuma Renda",
    "B": "Até R$ 1.320,00",
    "C": "De R$ 1.320,01 até R$ 1.980,00",
    "D": "De R$ 1.980,01 até R$ 2.640,00",
    "E": "De R$ 2.640,01 até R$ 3.300,00",
    "F": "De R$ 3.300,01 até R$ 3.960,00",
    "G": "De R$ 3.960,01 até R$ 5.280,00",
    "H": "De R$ 5.280,01 até R$ 6.600,00",
    "I": "De R$ 6.600,01 até R$ 7.920,00",
    "J": "De R$ 7.920,01 até R$ 9.240,00",
    "K": "De R$ 9.240,01 até R$ 10.560,00",
    "L": "De R$ 10.560,01 até R$ 11.880,00",
    "M": "De R$ 11.880,01 até R$ 13.200,00",
    "N": "De R$ 13.200,01 até R$ 15.840,00",
    "O": "De R$ 15.840,01 até R$19.800,00",
    "P": "De R$ 19.800,01 até R$ 26.400,00",
    "Q": "Acima de R$ 26.400,00"
}

valores_Q007 = {
    "A": "Não.",
    "B": "Sim, um ou dois dias por semana.",
    "C": "Sim, três ou quatro dias por semana.",
    "D": "Sim, pelo menos cinco dias por semana."
}

valores_Q008 = {
    "A": "Não.",
    "B": "Sim, um.",
    "C": "Sim, dois.",
    "D": "Sim, três.",
    "E": "Sim, quatro ou mais."
}

valores_Q009 = {
    "A": "Não.",
    "B": "Sim, um.",
    "C": "Sim, dois.",
    "D": "Sim, três.",
    "E": "Sim, quatro ou mais."
}

valores_Q010 = {
    "A": "Não.",
    "B": "Sim, um.",
    "C": "Sim, dois.",
    "D": "Sim, três.",
    "E": "Sim, quatro ou mais."
}

valores_Q011 = {
    "A": "Não.",
    "B": "Sim, uma.",
    "C": "Sim, duas.",
    "D": "Sim, três.",
    "E": "Sim, quatro ou mais."
}

valores_Q012 = {
    "A": "Não.",
    "B": "Sim, uma.",
    "C": "Sim, duas.",
    "D": "Sim, três.",
    "E": "Sim, quatro ou mais."
}

valores_Q013 = {
    "A": "Não.",
    "B": "Sim, um.",
    "C": "Sim, dois.",
    "D": "Sim, três.",
    "E": "Sim, quatro ou mais."
}

valores_Q014 = {
    "A": "Não.",
    "B": "Sim, uma.",
    "C": "Sim, duas.",
    "D": "Sim, três.",
    "E": "Sim, quatro ou mais."
}

valores_Q015 = {
    "A": "Não.",
    "B": "Sim, uma.",
    "C": "Sim, duas.",
    "D": "Sim, três.",
    "E": "Sim, quatro ou mais."
}

valores_Q016 = {
    "A": "Não.",
    "B": "Sim, um.",
    "C": "Sim, dois.",
    "D": "Sim, três.",
    "E": "Sim, quatro ou mais."
}

valores_Q017 = {
    "A": "Não.",
    "B": "Sim, uma.",
    "C": "Sim, duas.",
    "D": "Sim, três.",
    "E": "Sim, quatro ou mais."
}

valores_Q018 = {
    "A": "Não.",
    "B": "Sim."
}

valores_Q019 = {
    "A": "Não.",
    "B": "Sim, uma.",
    "C": "Sim, duas.",
    "D": "Sim, três.",
    "E": "Sim, quatro ou mais."
}

valores_Q020 = {
    "A": "Não.",
    "B": "Sim."
}

valores_Q021 = {
    "A": "Não.",
    "B": "Sim."
}

valores_Q022 = {
    "A": "Não.",
    "B": "Sim, um.",
    "C": "Sim, dois.",
    "D": "Sim, três.",
    "E": "Sim, quatro ou mais."
}

valores_Q023 = {
    "A": "Não.",
    "B": "Sim."
}

valores_Q024 = {
    "A": "Não.",
    "B": "Sim, um.",
    "C": "Sim, dois.",
    "D": "Sim, três.",
    "E": "Sim, quatro ou mais."
}

valores_Q025 = {
    "A": "Não.",
    "B": "Sim."
}

# Dicionários para variáveis demográficas
valores_TP_FAIXA_ETARIA = {
    1: "Menor de 17 anos",
    2: "17 anos",
    3: "18 anos",
    4: "19 anos",
    5: "20 anos",
    6: "21 anos",
    7: "22 anos",
    8: "23 anos",
    9: "24 anos",
    10: "25 anos",
    11: "Entre 26 e 30 anos",
    12: "Entre 31 e 35 anos",
    13: "Entre 36 e 40 anos",
    14: "Entre 41 e 45 anos",
    15: "Entre 46 e 50 anos",
    16: "Entre 51 e 55 anos",
    17: "Entre 56 e 60 anos",
    18: "Entre 61 e 65 anos",
    19: "Entre 66 e 70 anos",
    20: "Maior de 70 anos"
}

valores_TP_SEXO = {
    "M": "Masculino",
    "F": "Feminino"
}

valores_TP_ESTADO_CIVIL = {
    0: "Não informado",
    1: "Solteiro(a)",
    2: "Casado(a)/Mora com companheiro(a)",
    3: "Divorciado(a)/Desquitado(a)/Separado(a)",
    4: "Viúvo(a)"
}

valores_TP_COR_RACA = {
    0: "Não declarado",
    1: "Branca",
    2: "Preta",
    3: "Parda",
    4: "Amarela",
    5: "Indígena",
    6: "Não dispõe da informação"
}

valores_TP_ESCOLA = {
    1: "Não Respondeu",
    2: "Pública",
    3: "Privada"
}

# Dicionário geral de traduções dos valores das variáveis
valores_variaveis = {
    "Q001": valores_Q001,
    "Q002": valores_Q002,
    "Q003": valores_Q003,
    "Q004": valores_Q004,
    "Q005": valores_Q005,
    "Q006": valores_Q006,
    "Q007": valores_Q007,
    "Q008": valores_Q008,
    "Q009": valores_Q009,
    "Q010": valores_Q010,
    "Q011": valores_Q011,
    "Q012": valores_Q012,
    "Q013": valores_Q013,
    "Q014": valores_Q014,
    "Q015": valores_Q015,
    "Q016": valores_Q016,
    "Q017": valores_Q017,
    "Q018": valores_Q018,
    "Q019": valores_Q019,
    "Q020": valores_Q020,
    "Q021": valores_Q021,
    "Q022": valores_Q022,
    "Q023": valores_Q023,
    "Q024": valores_Q024,
    "Q025": valores_Q025,
    "TP_FAIXA_ETARIA": valores_TP_FAIXA_ETARIA,
    "TP_SEXO": valores_TP_SEXO,
    "TP_ESTADO_CIVIL": valores_TP_ESTADO_CIVIL,
    "TP_COR_RACA": valores_TP_COR_RACA,
    "TP_ESCOLA": valores_TP_ESCOLA
}

import math

# Dicionário de pontuações para cada variável
pontuacao_socioeconomica = {
    # Educação dos pais (Q001 e Q002)
    "Q001": {
        "A": 1.43,  # 10/7 (7 categorias válidas, ignorando "H")
        "B": 2.86,
        "C": 4.29,
        "D": 5.71,
        "E": 7.14,
        "F": 8.57,
        "G": 10.00,
        "H": 0  # "Não sei" = 0
    },
    "Q002": {
        "A": 1.43,  # 10/7 (7 categorias válidas, ignorando "H")
        "B": 2.86,
        "C": 4.29,
        "D": 5.71,
        "E": 7.14,
        "F": 8.57,
        "G": 10.00,
        "H": 0  # "Não sei" = 0
    },

    # Ocupação dos pais (Q003 e Q004)
    "Q003": {
        "A": 2.00,  # 10/5 (5 grupos válidos, ignorando "F")
        "B": 4.00,
        "C": 6.00,
        "D": 8.00,
        "E": 10.00,
        "F": 0  # "Não sei" = 0
    },
    "Q004": {
        "A": 2.00,
        "B": 4.00,
        "C": 6.00,
        "D": 8.00,
        "E": 10.00,
        "F": 0
    },

    # Número de pessoas na residência (Q005) - INVERTIDO
    "Q005": {
        "1": 10.00,  # Morar sozinho = melhor situação
        "2": 9.00,
        "3": 8.00,
        "4": 7.00,
        "5": 6.00,
        "6": 5.00,
        "7": 4.00,
        "8": 3.00,
        "9": 2.00,
        "10": 1.00,
        "11": 0.91,
        "12": 0.83,
        "13": 0.77,
        "14": 0.71,
        "15": 0.67,
        "16": 0.63,
        "17": 0.59,
        "18": 0.56,
        "19": 0.53,
        "20": 0.50  # 20 pessoas = pior situação
    },

    # Renda familiar (Q006)
    "Q006": {
        "A": 0.59,  # 10/17 categorias
        "B": 1.18,
        "C": 1.76,
        "D": 2.35,
        "E": 2.94,
        "F": 3.53,
        "G": 4.12,
        "H": 4.71,
        "I": 5.29,
        "J": 5.88,
        "K": 6.47,
        "L": 7.06,
        "M": 7.65,
        "N": 8.24,
        "O": 8.82,
        "P": 9.41,
        "Q": 10.00  # Maior renda
    },

    # Empregado doméstico (Q007)
    "Q007": {
        "A": 2.50,  # 10/4 categorias
        "B": 5.00,
        "C": 7.50,
        "D": 10.00  # Empregado 5+ dias/semana
    },

    # Bens e comodidades (todas com mesmo padrão)
    "Q008": {  # Banheiros
        "A": 2.00, "B": 4.00, "C": 6.00, "D": 8.00, "E": 10.00
    },
    "Q009": {  # Quartos
        "A": 2.00, "B": 4.00, "C": 6.00, "D": 8.00, "E": 10.00
    },
    "Q010": {  # Carros
        "A": 2.00, "B": 4.00, "C": 6.00, "D": 8.00, "E": 10.00
    },
    "Q011": {  # Motos
        "A": 2.00, "B": 4.00, "C": 6.00, "D": 8.00, "E": 10.00
    },
    "Q012": {  # Geladeiras
        "A": 2.00, "B": 4.00, "C": 6.00, "D": 8.00, "E": 10.00
    },
    "Q013": {  # Freezers
        "A": 2.00, "B": 4.00, "C": 6.00, "D": 8.00, "E": 10.00
    },
    "Q014": {  # Máquina de lavar
        "A": 2.00, "B": 4.00, "C": 6.00, "D": 8.00, "E": 10.00
    },
    "Q015": {  # Máquina de secar
        "A": 2.00, "B": 4.00, "C": 6.00, "D": 8.00, "E": 10.00
    },
    "Q016": {  # Microondas
        "A": 2.00, "B": 4.00, "C": 6.00, "D": 8.00, "E": 10.00
    },
    "Q017": {  # Máquina de lavar louça
        "A": 2.00, "B": 4.00, "C": 6.00, "D": 8.00, "E": 10.00
    },
    "Q018": {  # Aspirador de pó
        "A": 0, "B": 10.00  # Binária
    },
    "Q019": {  # TVs
        "A": 2.00, "B": 4.00, "C": 6.00, "D": 8.00, "E": 10.00
    },
    "Q020": {  # DVD
        "A": 0, "B": 10.00  # Binária
    },
    "Q021": {  # TV por assinatura
        "A": 0, "B": 10.00  # Binária
    },
    "Q022": {
        "A": 0,  # Nenhum celular = pior situação
        "B": 2.50,
        "C": 5.00,
        "D": 7.50,
        "E": 10.00  # 4+ celulares = melhor situação
    },
    "Q023": {  # Telefone fixo
        "A": 0, "B": 10.00  # Binária
    },
    "Q024": {  # Computadores
        "A": 2.00, "B": 4.00, "C": 6.00, "D": 8.00, "E": 10.00
    },
    "Q025": {  # Internet
        "A": 0, "B": 10.00  # Binária
    }
}


def calcular_pontuacao(respostas):
    """
    Calcula a pontuação socioeconômica com base nas respostas do questionário.

    Args:
        respostas (dict): Dicionário com as respostas (ex: {"Q001": "A", "Q002": "B", ...})

    Returns:
        float: Pontuação total normalizada (0-100)
    """
    total = 0
    max_possivel = 0

    for var, dic_pontos in pontuacao_socioeconomica.items():
        if var in respostas:
            resposta = str(respostas[var])  # Garante que é string
            if resposta in dic_pontos:
                total += dic_pontos[resposta]
                max_possivel += 10  # Cada variável contribui no máximo 10

    if max_possivel == 0:
        return 0

    return (total / max_possivel) * 100  # Normaliza para 0-100