from funcoes import (
    carregar_dados, padronizar_categoria, padronizar_canal,
    validar_quantidade, validar_preco, marcar_problemas
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

if __name__ == "__main__":
    main()