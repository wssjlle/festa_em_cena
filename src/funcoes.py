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
    
    # Flag: houve qualquer alteração em relação ao original (espaços, caixa, etc.)
    original_limpo = original.str.strip().str.lower()
        # Flag: o valor original (antes de qualquer limpeza) era diferente do final
    df["canal_padronizado"] = original != df["canal_padrao"]
    
    return df