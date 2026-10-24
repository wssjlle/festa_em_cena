from funcoes import carregar_dados, padronizar_categoria, padronizar_canal

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
    
    print("\nCategorias limpas únicas:")
    print(sorted(df["categoria_limpa"].unique()))
    
    print("\nCanais padronizados únicos:")
    print(df["canal_padrao"].value_counts(dropna=False))

if __name__ == "__main__":
    main()