from funcoes import carregar_dados

def main():
    caminho = "dados/halloween_vendas.csv"
    df = carregar_dados(caminho)

    print("=== Verificação inicial ===")
    print(f"Total de linhas: {df.shape[0]}")
    print(f"Total de colunas: {df.shape[1]}")
    print("\nPrimeiras 3 linhas:")
    print(df.head(3))
    print("\nTipos das colunas (após leitura):")
    print(df.dtypes)

if __name__ == "__main__":
    main()