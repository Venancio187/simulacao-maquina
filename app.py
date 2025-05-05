import csv
import json
from datetime import datetime

def carregar_insumos(caminho):
    with open(caminho, mode='r', newline='') as csvfile:
        leitor = csv.DictReader(csvfile)
        return list(leitor)

def salvar_op_ativa(dados_op):
    with open("op_ativa.json", "w") as jsonfile:
        json.dump(dados_op, jsonfile, indent=4)

def menu_interativo(insumos):
    print("\n=== MENU DE ORDENS DE PRODUÇÃO ===")
    for idx, op in enumerate(insumos):
        print(f"[{idx}] OP: {op['op']} | Produto: {op['produto']} | Quantidade: {op['quantidade']}")

    while True:
        try:
            escolha = int(input("\nDigite o número da OP desejada: "))
            if 0 <= escolha < len(insumos):
                break
            else:
                print("❌ Número fora do intervalo. Tente novamente.")
        except ValueError:
            print("❌ Entrada inválida. Digite um número.")

    op_escolhida = insumos[escolha]
    op_escolhida["data"] = datetime.now().strftime("%d/%m/%Y")  # Data ilustrativa

    salvar_op_ativa(op_escolhida)
    print("\n✅ OP ativa salva com sucesso em op_ativa.json")

if __name__ == "__main__":
    caminho_csv = "insumos.csv"
    insumos = carregar_insumos(caminho_csv)
    if not insumos:
        print("⚠️ Nenhuma OP encontrada no arquivo CSV.")
    else:
        menu_interativo(insumos)
