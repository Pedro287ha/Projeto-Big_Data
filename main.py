import pandas as pd
import matplotlib.pyplot as plt



def gerar_pdf_atualizado():
    pass


def filtrar_dados():
    pass


def main():
    
    try:
        arquivo = 'dados_restaurante.csv'

    
        dados = pd.read_csv(arquivo)
        
        print(dados)
    
    except FileNotFoundError:
        print("Arquivo NAO encontrado!")


if __name__ == "__main__":
    main()



