"""
Módulo de funções para limpeza e validação dos dados da Festa em Cena.

Decisões gerais:
- Todos os dados são lidos inicialmente como texto para evitar conversões automáticas.
- Problemas são marcados com flags booleanas em vez de imputar ou remover valores.
- O arquivo original nunca é alterado; trabalhamos sempre com cópias do DataFrame.
"""

import re
import pandas as pd

def carregar_dados(caminho: str) -> pd.DataFrame:
    """
    Lê o CSV forçando todas as colunas como texto.

    Parâmetros
    ----------
    caminho : str
        Caminho para o arquivo halloween_vendas.csv.

    Retorna
    -------
    pd.DataFrame
        DataFrame com todas as colunas como string.
        Valores vazios permanecem como string vazia (não viram NaN automático).
    """

    df = pd.read_csv(
        caminho,
        dtype=str,
        encoding="utf-8",
        keep_default_na=False  # vazio continua como string vazia, não vira NaN automático
    )
    return df


def padronizar_categoria(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa e padroniza a coluna categoria.

    Regras aplicadas:
    - strip() e lower()
    - re.sub para remover qualquer caractere que não seja letra ou espaço
    - valores que ficam vazios após a limpeza viram "sem categoria"

    Cria as colunas:
    - categoria_limpa
    - categoria_vazia_preenchida (flag)
    - categoria_alterada (flag)
    """

    df = df.copy()
    
    original = df["categoria"].fillna("").astype(str)
    
    # Limpeza: remove pontuação e normaliza caixa/espaços
    limpa = original.str.strip().str.lower()
    limpa = limpa.apply(lambda x: re.sub(r"[^a-z ]", "", x).strip())
    limpa = limpa.replace("", "sem categoria")
    
    df["categoria_limpa"] = limpa
    
    # Flags de contagem (critério documentado no README)
    df["categoria_vazia_preenchida"] = original.str.strip() == ""
    df["categoria_alterada"] = (
        (original.str.strip() != "") & 
        (original.str.strip().str.lower() != df["categoria_limpa"])
    )
    
    return df


def padronizar_canal(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza a coluna canal_venda para os valores oficiais:
    Mercado, Loja física e Web.

    Cria as colunas:
    - canal_padrao
    - canal_padronizado (flag)
    """

    df = df.copy()
    
    original = df["canal_venda"].fillna("").astype(str)
    limpo = original.str.strip().str.lower()
    
    # Mapeamento direto (mais seguro que remover acentos)
    mapa = {
        "mercado": "Mercado",
        "loja fisica": "Loja física",
        "loja física": "Loja física",
        "web": "Web",
    }
    
    # Também captura variações com espaços extras
    df["canal_padrao"] = limpo.map(mapa)
    
    # Se ainda não mapeou, tenta uma limpeza mais leve
    nao_mapeado = df["canal_padrao"].isna()
    limpo2 = limpo.str.replace(r"\s+", " ", regex=True).str.strip()
    df.loc[nao_mapeado, "canal_padrao"] = limpo2[nao_mapeado].map(mapa)
    

    # Flag: o valor original (antes de qualquer limpeza) era diferente do final
    df["canal_padronizado"] = original != df["canal_padrao"]
    
    return df

def validar_quantidade(df: pd.DataFrame) -> pd.DataFrame:
    """
    Marca erro_quantidade quando o valor não é um inteiro maior que zero.

    Não imputa valores; apenas cria a flag booleana.
    """

    df = df.copy()
    
    # Tenta converter para número
    qtd = pd.to_numeric(df["quantidade"], errors="coerce")
    
    df["erro_quantidade"] = (
        qtd.isna() |              # não é número
        (qtd <= 0) |              # zero ou negativo
        (qtd != qtd.astype(int))  # não é inteiro
    )
    return df


def validar_preco(df: pd.DataFrame) -> pd.DataFrame:
    """
    Marca erro_preco quando o preço está ausente ou é negativo.

    Não imputa valores; apenas cria a flag booleana.
    """

    df = df.copy()
    
    preco = pd.to_numeric(df["preco_unitario"], errors="coerce")
    
    df["erro_preco"] = preco.isna() | (preco < 0)
    return df


def marcar_problemas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria a flag tem_problema (verdadeiro se houver erro de quantidade ou de preço).
    """

    df = df.copy()
    df["tem_problema"] = df["erro_quantidade"] | df["erro_preco"]
    return df

def tratar_datas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte data_venda para datetime e cria versão no formato brasileiro.

    Datas inválidas são marcadas com a flag erro_data e não são substituídas.
    """

    df = df.copy()
    
    df["data_venda_dt"] = pd.to_datetime(df["data_venda"], errors="coerce")
    df["erro_data"] = df["data_venda_dt"].isna()
    
    # Formato brasileiro
    df["data_br"] = df["data_venda_dt"].dt.strftime("%d/%m/%Y")
    
    # Componentes úteis para o agrupamento
    df["ano"] = df["data_venda_dt"].dt.year
    df["mes"] = df["data_venda_dt"].dt.month
    df["hora"] = df["data_venda_dt"].dt.hour
    
    return df


def investigar_entrega(df: pd.DataFrame) -> pd.DataFrame:
    """
    Investiga a hipótese: todo pedido sem data_entrega é Cancelado.

    Cria as flags:
    - sem_data_entrega
    - entrega_e_cancelado
    - entrega_nao_cancelado (contraexemplos)
    """
    
    df = df.copy()
    
    sem_entrega = df["data_entrega"].fillna("").str.strip() == ""
    cancelado = df["status_pedido"].str.strip() == "Cancelado"
    
    df["sem_data_entrega"] = sem_entrega
    df["entrega_e_cancelado"] = sem_entrega & cancelado
    df["entrega_nao_cancelado"] = sem_entrega & ~cancelado
    
    return df