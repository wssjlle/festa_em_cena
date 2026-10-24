import pandas as pd
from funcoes import (
    carregar_dados, padronizar_categoria, padronizar_canal,
    validar_quantidade, validar_preco, marcar_problemas,
    tratar_datas, investigar_entrega
)

def main():
    caminho = "dados/halloween_vendas.csv"
    df = carregar_dados(caminho)
    
    print("=== Verificação inicial ===")
    print(f"Total de linhas: {df.shape[0]}")
    
    # Sprint 2
    df = padronizar_categoria(df)
    df = padronizar_canal(df)
    
    print("\n=== Contagens de padronização ===")
    print(f"Categorias vazias preenchidas: {df['categoria_vazia_preenchida'].sum()}")
    print(f"Categorias alteradas (não vazias): {df['categoria_alterada'].sum()}")
    print(f"Canais padronizados: {df['canal_padronizado'].sum()}")
    
    # Sprint 3
    df = validar_quantidade(df)
    df = validar_preco(df)
    df = marcar_problemas(df)
    
    print("\n=== Validação de quantidade e preço ===")
    print(f"Erros de quantidade: {df['erro_quantidade'].sum()}")
    print(f"Erros de preço: {df['erro_preco'].sum()}")
    print(f"Pedidos com algum problema: {df['tem_problema'].sum()}")
    
    # Verifica se há sobreposição
    print("\nDistribuição dos erros (sem sobreposição esperada):")
    print(df[["erro_quantidade", "erro_preco"]].value_counts())

    # Sprint 4
    df = tratar_datas(df)
    df = investigar_entrega(df)
    
    print("\n=== Datas ===")
    print(f"Datas de venda inválidas: {df['erro_data'].sum()}")
    
    print("\n=== Regra de negócio: sem data de entrega ===")
    print(f"Pedidos sem data de entrega: {df['sem_data_entrega'].sum()}")
    print(f"  → Cancelados: {df['entrega_e_cancelado'].sum()}")
    print(f"  → Outros status: {df['entrega_nao_cancelado'].sum()}")
    
    print("\nTabela cruzada (status × tem data de entrega):")
    tabela = pd.crosstab(
        df["status_pedido"],
        df["sem_data_entrega"],
        margins=True
    )
    print(tabela)
    
    print("\nExemplos de pedidos sem entrega e não cancelados:")
    exemplos = df[df["entrega_nao_cancelado"]][["pedido_id", "status_pedido", "data_entrega"]].head(3)
    print(exemplos)
    
    print("\n=== Contagem por canal (todos os status) ===")
    print(df["canal_padrao"].value_counts())
    
    print("\n=== Contagem por ano-mês (apenas datas válidas) ===")
    validos = df[~df["erro_data"]]
    print(validos.groupby(["ano", "mes"]).size().unstack(fill_value=0))

if __name__ == "__main__":
    main()