class Fisicos:
    def __init__(self, imagem, nome, ingredientes, peso, preco, acompanhamento):
        self.imagem = imagem
        self.nome = nome
        self.ingredientes = ingredientes
        self.peso = peso
        self.preco = preco
        self.acompanhamento = acompanhamento

class Liquidos:
    def __init__(self, imagem, nome, volume, preco, acompanhamento):
        self.imagem = imagem
        self.nome = nome
        self.volume = volume
        self.preco = preco
        self.acompanhamento = acompanhamento

fisicos = []
liquidos = []
acompanhamentos = []

def criarfisicos():
    imagem = input("Imagem: ")
    nome = input("Nome: ")
    ingredientes = input("Ingredientes: ")
    peso = float(input("Peso: "))
    preco = float(input("Preço: "))
    acompanhamento = input("Acompanhamento (Sim/Não): ")
    
    novo_fisico = Fisicos(imagem, nome, ingredientes, peso, preco, acompanhamento)
    fisicos.append(novo_fisico)
    if acompanhamento.lower() == "sim":
        acompanhamentos.append(novo_fisico)
    print("Produto Físico Criado!")

def criarliquidos():
    imagem = input("Imagem: ")
    nome = input("Nome: ")
    volume = float(input("Volume: "))
    preco = float(input("Preço: "))
    acompanhamento = input("Acompanhamento (Sim/Não): ")
    
    novo_liquido = Liquidos(imagem, nome, volume, preco, acompanhamento)
    liquidos.append(novo_liquido)
    if acompanhamento.lower() == "sim":
        acompanhamentos.append(novo_liquido)
    print("Produto Líquido Criado!")

def mostrar_produtos():
    print("\nProdutos Físicos:")
    for f in fisicos:
        print(f"Nome: {f.nome}, Preço: {f.preco}")

    print("\nProdutos Líquidos:")
    for l in liquidos:
        print(f"Nome: {l.nome}, Preço: {l.preco}")

    print("\nAcompanhamentos:")
    for a in acompanhamentos:
        print(f"Nome: {a.nome}, Preço: {a.preco}")

def editar_produtos():
    print("\nProdutos Físicos:")
    for idx, f in enumerate(sorted(fisicos, key=lambda x: x.nome)):
        print(f"{idx + 1}. {f.nome}")
    
    print("\nProdutos Líquidos:")
    for idx, l in enumerate(sorted(liquidos, key=lambda x: x.nome)):
        print(f"{idx + 1}. {l.nome}")
    
    print("\nAcompanhamentos:")
    for idx, a in enumerate(sorted(acompanhamentos, key=lambda x: x.nome)):
        print(f"{idx + 1}. {a.nome}")
    
    tipo = input("\nEscolha o tipo de produto para editar (Fisicos/Liquidos/Acompanhamentos): ").lower()
    if tipo == "fisicos":
        produtos = sorted(fisicos, key=lambda x: x.nome)
    elif tipo == "liquidos":
        produtos = sorted(liquidos, key=lambda x: x.nome)
    elif tipo == "acompanhamentos":
        produtos = sorted(acompanhamentos, key=lambda x: x.nome)
    else:
        print("Tipo de produto inválido.")
        return

    idx = int(input("Escolha o número do produto para editar: ")) - 1
    if idx < 0 or idx >= len(produtos):
        print("Número de produto inválido.")
        return

    produto = produtos[idx]
    print(f"Editando {produto.nome}...")

    produto.imagem = input(f"Imagem ({produto.imagem}): ") or produto.imagem
    produto.nome = input(f"Nome ({produto.nome}): ") or produto.nome
    if tipo == "fisicos":
        produto.ingredientes = input(f"Ingredientes ({produto.ingredientes}): ") or produto.ingredientes
        produto.peso = input(f"Peso ({produto.peso}): ") or produto.peso
    else:
        produto.volume = input(f"Volume ({produto.volume}): ") or produto.volume
    produto.preco = input(f"Preço ({produto.preco}): ") or produto.preco
    acompanhamento = input(f"Acompanhamento ({produto.acompanhamento}): ") or produto.acompanhamento
    if acompanhamento.lower() == "sim" and produto not in acompanhamentos:
        acompanhamentos.append(produto)
    elif acompanhamento.lower() == "não" and produto in acompanhamentos:
        acompanhamentos.remove(produto)
    produto.acompanhamento = acompanhamento

    print("Produto atualizado!")

def BotaoExcluir():
    tipo = input("Escolha o tipo de produto para excluir (Fisicos/Liquidos/Acompanhamentos): ").lower()
    if tipo == "fisicos":
        produtos = fisicos
    elif tipo == "liquidos":
        produtos = liquidos
    elif tipo == "acompanhamentos":
        produtos = acompanhamentos
    else:
        print("Tipo de produto inválido.")
        return

    idx = int(input("Escolha o número do produto para excluir: ")) - 1
    if idx < 0 or idx >= len(produtos):
        print("Número de produto inválido.")
        return

    produto = produtos[idx]
    resposta = input(f"Deseja realmente excluir {produto.nome}? (Sim/Não): ").lower()
    if resposta == "sim":
        produtos.remove(produto)
        if produto in acompanhamentos:
            acompanhamentos.remove(produto)
        print(f"{produto.nome} removido!")
    else:
        print(f"{produto.nome} não removido.")

def verificar_credenciais():
    email = input("Digite seu e-mail: ")
    nome = input("Digite seu nome: ")
    senha = input("Digite sua senha: ")
    confirmar_senha = input("Confirme sua senha: ")

    if senha == "PizzaBoa" and senha == confirmar_senha:
        print(f"\nBem-vindo, {nome}!")
        return nome
    else:
        print("Senha incorreta. Tente novamente.")
        return verificar_credenciais()

def menu_principal(nome):
    while True:
        print(f"\n{nome} - Menu Principal")
        print("1. +Criar")
        print("2. Estoque")
        print("3. Menu")
        print("4. Editar")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")
        if escolha == "1":
            sub_escolha = input("Criar Físicos ou Criar Líquidos: ").lower()
            if sub_escolha == "criar fisicos":
                criarfisicos()
            elif sub_escolha == "criar liquidos":
                criarliquidos()
            else:
                print("Opção inválida.")
        elif escolha == "2":
            mostrar_produtos()
        elif escolha == "3":
            mostrar_produtos()
        elif escolha == "4":
            editar_produtos()
        elif escolha == "5":
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    nome_usuario = verificar_credenciais()
    menu_principal(nome_usuario)
