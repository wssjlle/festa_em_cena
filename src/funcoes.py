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