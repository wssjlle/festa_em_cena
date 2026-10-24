import re
import pandas as pd

def carregar_dados(caminho: str) -> pd.DataFrame:
    """
    Lê o CSV forçando todas as colunas como texto.
    Isso evita conversões automáticas indesejadas e deixa o tratamento sob nosso controle.
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
    Limpa a coluna categoria:
    - strip + lower
    - re.sub para remover pontuação indevida
    - preenche vazios com 'sem categoria'
    """
    df = df.copy()
    
    original = df["categoria"].fillna("").astype(str)
    
    # Limpeza
    limpa = original.str.strip().str.lower()
    limpa = limpa.apply(lambda x: re.sub(r"[^a-z ]", "", x).strip())
    limpa = limpa.replace("", "sem categoria")
    
    df["categoria_limpa"] = limpa
    
    # Contagens alinhadas ao enunciado
    df["categoria_vazia_preenchida"] = original.str.strip() == ""
    df["categoria_alterada"] = (
        (original.str.strip() != "") & 
        (original.str.strip().str.lower() != df["categoria_limpa"])
    )
    
    return df


def padronizar_canal(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza canal_venda para: Mercado, Loja física, Web.
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
    """
    df = df.copy()
    
    # Tenta converter para número
    qtd = pd.to_numeric(df["quantidade"], errors="coerce")
    
    df["erro_quantidade"] = (
        qtd.isna() |          # não é número
        (qtd <= 0) |          # zero ou negativo
        (qtd != qtd.astype(int))  # não é inteiro
    )
    return df


def validar_preco(df: pd.DataFrame) -> pd.DataFrame:
    """
    Marca erro_preco quando o preço está ausente ou é negativo.
    """
    df = df.copy()
    
    preco = pd.to_numeric(df["preco_unitario"], errors="coerce")
    
    df["erro_preco"] = preco.isna() | (preco < 0)
    return df


def marcar_problemas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria a flag tem_problema (qualquer erro de quantidade ou preço).
    """
    df = df.copy()
    df["tem_problema"] = df["erro_quantidade"] | df["erro_preco"]
    return df

def tratar_datas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte data_venda para datetime e cria versão brasileira.
    Marca datas inválidas.
    """
    df = df.copy()
    
    df["data_venda_dt"] = pd.to_datetime(df["data_venda"], errors="coerce")
    df["erro_data"] = df["data_venda_dt"].isna()
    
    # Formato brasileiro
    df["data_br"] = df["data_venda_dt"].dt.strftime("%d/%m/%Y")
    
    # Componentes úteis
    df["ano"] = df["data_venda_dt"].dt.year
    df["mes"] = df["data_venda_dt"].dt.month
    df["hora"] = df["data_venda_dt"].dt.hour
    
    return df


def investigar_entrega(df: pd.DataFrame) -> pd.DataFrame:
    """
    Investiga se todo pedido sem data_entrega é Cancelado.
    Cria flags e retorna o DataFrame enriquecido.
    """
    df = df.copy()
    
    sem_entrega = df["data_entrega"].fillna("").str.strip() == ""
    cancelado = df["status_pedido"].str.strip() == "Cancelado"
    
    df["sem_data_entrega"] = sem_entrega
    df["entrega_e_cancelado"] = sem_entrega & cancelado
    df["entrega_nao_cancelado"] = sem_entrega & ~cancelado
    
    return df