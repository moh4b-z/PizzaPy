import tkinter as tk
from tkinter import messagebox
import json
import datetime

class Fisicos:
    def __init__(self, imagem, nome, ingredientes, peso, preco, acompanhamento):
        self.imagem = imagem
        self.nome = nome
        self.ingredientes = ingredientes
        self.peso = peso
        self.preco = preco
        self.acompanhamento = acompanhamento

    def to_dict(self):
        return {
            "tipo": "fisicos",
            "imagem": self.imagem,
            "nome": self.nome,
            "ingredientes": self.ingredientes,
            "peso": self.peso,
            "preco": self.preco,
            "acompanhamento": self.acompanhamento
        }

class Liquidos:
    def __init__(self, imagem, nome, volume, preco, acompanhamento):
        self.imagem = imagem
        self.nome = nome
        self.volume = volume
        self.preco = preco
        self.acompanhamento = acompanhamento

    def to_dict(self):
        return {
            "tipo": "liquidos",
            "imagem": self.imagem,
            "nome": self.nome,
            "volume": self.volume,
            "preco": self.preco,
            "acompanhamento": self.acompanhamento
        }

fisicos = []
liquidos = []
acompanhamentos = []

def salvar_produtos():
    produtos = [p.to_dict() for p in fisicos + liquidos]
    with open('produtos.txt', 'w', encoding='utf-8') as arquivo:
        json.dump(produtos, arquivo, ensure_ascii=False)

def carregar_produtos():
    try:
        with open('produtos.txt', 'r', encoding='utf-8') as arquivo:
            produtos = json.load(arquivo)
            for p in produtos:
                if p["tipo"] == "fisicos":
                    produto = Fisicos(p["imagem"], p["nome"], p["ingredientes"], p["peso"], p["preco"], p["acompanhamento"])
                    fisicos.append(produto)
                elif p["tipo"] == "liquidos":
                    produto = Liquidos(p["imagem"], p["nome"], p["volume"], p["preco"], p["acompanhamento"])
                    liquidos.append(produto)
                if p["acompanhamento"].lower() == "sim":
                    acompanhamentos.append(produto)
    except FileNotFoundError:
        print("Erro: Arquivo não encontrado.")
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    except Exception as e:
        print(f"Um erro inesperado ocorreu: {e}")

class Aplicativo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicativo de Gerenciamento de Produtos")
        self.geometry("800x600")
        
        self.nome_usuario = "Usuário"
        self.log_atividades = []

        self.var_pesquisa = tk.StringVar()
        self.var_pesquisa.trace("w", self.atualizar_sugestoes_pesquisa)

        self.lista_sugestoes = tk.Listbox(self)
        self.lista_sugestoes.bind("<<ListboxSelect>>", self.selecionar_sugestao)

        self.criar_menu_principal()
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def criar_tela_login(self):
        self.quadro_login = tk.Frame(self)
        self.quadro_login.pack(pady=20)

        tk.Label(self.quadro_login, text="E-mail").pack()
        self.entrada_email = tk.Entry(self.quadro_login)
        self.entrada_email.pack()

        tk.Label(self.quadro_login, text="Nome").pack()
        self.entrada_nome = tk.Entry(self.quadro_login)
        self.entrada_nome.pack()

        tk.Label(self.quadro_login, text="Senha").pack()
        self.entrada_senha = tk.Entry(self.quadro_login, show="*")
        self.entrada_senha.pack()

        tk.Label(self.quadro_login, text="Confirme a Senha").pack()
        self.entrada_conf_senha = tk.Entry(self.quadro_login, show="*")
        self.entrada_conf_senha.pack()

        tk.Button(self.quadro_login, text="Login", command=self.verificar_credenciais).pack(pady=10)


    def verificar_credenciais(self):
        email = self.entrada_email.get()
        nome = self.entrada_nome.get()
        senha = self.entrada_senha.get()
        confirmar_senha = self.entrada_conf_senha.get()

        if senha == "PizzaBoa" and senha == confirmar_senha:
            self.nome_usuario = nome
            self.hora_entrada = datetime.datetime.now()
            self.log_atividades.append(f"{nome} fez login ({self.hora_entrada.strftime('%H:%M')})")
            messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {nome}!")
            self.quadro_login.destroy()
            self.criar_menu_principal()
        else:
            messagebox.showerror("Erro de Login", "Senha incorreta. Tente novamente.")

    def criar_menu_principal(self):
        self.limpar_quadro()

        self.quadro_menu = tk.Frame(self)
        self.quadro_menu.pack(pady=20)

        tk.Label(self.quadro_menu, text=f"{self.nome_usuario} - Menu Principal", font=("Helvetica", 16)).pack(pady=10)

        quadro_pesquisa_e_retorno = tk.Frame(self.quadro_menu)
        quadro_pesquisa_e_retorno.pack(fill=tk.X)

        self.criar_botao_retorno(quadro_pesquisa_e_retorno, self.criar_menu_principal)
        self.criar_barra_pesquisa(quadro_pesquisa_e_retorno)

        quadro_esquerdo = tk.Frame(self.quadro_menu)
        quadro_esquerdo.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        quadro_direito = tk.Frame(self.quadro_menu)
        quadro_direito.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        tk.Button(quadro_direito, text="+Criar", command=self.mostrar_menu_criar).pack(pady=5)
        tk.Button(quadro_direito, text="Estoque", command=self.mostrar_produtos).pack(pady=5)
        tk.Button(quadro_direito, text="Menu", command=self.mostrar_produtos).pack(pady=5)
        tk.Button(quadro_direito, text="Editar", command=self.editar_produtos).pack(pady=5)

        self.criar_exibicao_produtos(quadro_esquerdo, "Pizzas", fisicos)
        self.criar_exibicao_produtos(quadro_esquerdo, "Bebidas", liquidos)
        self.criar_exibicao_produtos(quadro_esquerdo, "Acompanhamentos", acompanhamentos)

    def limpar_quadro(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def criar_exibicao_produtos(self, parent, titulo, produtos):
        quadro = ctk.CTkFrame(parent)
        quadro.pack(pady=10, fill='x')
        ctk.CTkLabel(quadro, text=titulo, font=("Helvetica", 14)).pack(anchor='w')
        quadro_exibicao = ctk.CTkFrame(quadro)
        quadro_exibicao.pack()
        for produto in produtos[-3:]:
            self.exibir_produto(quadro_exibicao, produto)

    def exibir_produto(self, parent, produto):
        quadro_produto = ctk.CTkFrame(parent, width=50, height=50, border_width=1)
        quadro_produto.pack_propagate(False)
        quadro_produto.pack(side=ctk.LEFT, padx=5)

        rotulo_imagem = ctk.CTkLabel(quadro_produto, text=produto.imagem, width=30, height=30)
        rotulo_imagem.pack()
        rotulo_nome = ctk.CTkLabel(quadro_produto, text=produto.nome, wraplength=50)
        rotulo_nome.pack()
        quadro_produto.bind("<Button-1>", lambda e: self.editar_produto(produto))

    def criar_barra_pesquisa(self, parent):
        quadro_pesquisa = ctk.CTkFrame(parent)
        quadro_pesquisa.pack(side=ctk.RIGHT)
        ctk.CTkLabel(quadro_pesquisa, text="Pesquisar: ").pack(side=ctk.LEFT)
        self.var_pesquisa = ctk.StringVar()
        self.entrada_pesquisa = ctk.CTkEntry(quadro_pesquisa, textvariable=self.var_pesquisa)
        self.entrada_pesquisa.pack(side=ctk.LEFT)
        self.var_pesquisa.trace("w", self.atualizar_sugestoes_pesquisa)
        self.lista_sugestoes = ctk.CTkListbox(quadro_pesquisa)
        self.lista_sugestoes.pack(side=ctk.LEFT)
        self.lista_sugestoes.bind("<<ListboxSelect>>", self.selecionar_sugestao)

    def criar_botao_retorno(self, parent, comando):
        ctk.CTkButton(parent, text="Retornar", command=comando).pack(side=ctk.LEFT, padx=10)

    def mostrar_menu_criar(self):
        self.limpar_quadro()
        self.quadro_criar = ctk.CTkFrame(self)
        self.quadro_criar.pack(pady=20)

        ctk.CTkLabel(self.quadro_criar, text="Adicionar Produto").pack(pady=10)

        self.var_tipo_produto = ctk.StringVar(value="fisicos")
        ctk.CTkRadioButton(self.quadro_criar, text="Pizza", variable=self.var_tipo_produto, value="fisicos").pack()
        ctk.CTkRadioButton(self.quadro_criar, text="Bebida", variable=self.var_tipo_produto, value="liquidos").pack()

        self.var_imagem = ctk.StringVar()
        ctk.CTkLabel(self.quadro_criar, text="Imagem").pack()
        ctk.CTkEntry(self.quadro_criar, textvariable=self.var_imagem).pack()

        self.var_nome = ctk.StringVar()
        ctk.CTkLabel(self.quadro_criar, text="Nome").pack()
        ctk.CTkEntry(self.quadro_criar, textvariable=self.var_nome).pack()

        self.var_ingredientes = ctk.StringVar()
        ctk.CTkLabel(self.quadro_criar, text="Ingredientes (somente para Pizzas)").pack()
        ctk.CTkEntry(self.quadro_criar, textvariable=self.var_ingredientes).pack()

        self.var_peso = ctk.StringVar()
        ctk.CTkLabel(self.quadro_criar, text="Peso (somente para Pizzas)").pack()
        ctk.CTkEntry(self.quadro_criar, textvariable=self.var_peso).pack()

        self.var_volume = ctk.StringVar()
        ctk.CTkLabel(self.quadro_criar, text="Volume (somente para Bebidas)").pack()
        ctk.CTkEntry(self.quadro_criar, textvariable=self.var_volume).pack()

        self.var_preco = ctk.StringVar()
        ctk.CTkLabel(self.quadro_criar, text="Preço").pack()
        ctk.CTkEntry(self.quadro_criar, textvariable=self.var_preco).pack()

        self.var_acompanhamento = ctk.StringVar(value="não")
        ctk.CTkRadioButton(self.quadro_criar, text="Sim", variable=self.var_acompanhamento, value="sim").pack()
        ctk.CTkRadioButton(self.quadro_criar, text="Não", variable=self.var_acompanhamento, value="não").pack()

        ctk.CTkButton(self.quadro_criar, text="Salvar", command=self.salvar_novo_produto).pack(pady=10)
        ctk.CTkButton(self.quadro_criar, text="Cancelar", command=self.criar_menu_principal).pack(pady=10)

    def salvar_novo_produto(self):
        tipo = self.var_tipo_produto.get()
        imagem = self.var_imagem.get()
        nome = self.var_nome.get()
        preco = self.var_preco.get()
        acompanhamento = self.var_acompanhamento.get()

        if tipo == "fisicos":
            ingredientes = self.var_ingredientes.get()
            peso = self.var_peso.get()
            novo_produto = Fisicos(imagem, nome, ingredientes, peso, preco, acompanhamento)
            fisicos.append(novo_produto)
        else:
            volume = self.var_volume.get()
            novo_produto = Liquidos(imagem, nome, volume, preco, acompanhamento)
            liquidos.append(novo_produto)

        if acompanhamento.lower() == "sim":
            acompanhamentos.append(novo_produto)

        salvar_produtos()
        self.log_atividades.append(f"{self.nome_usuario} adicionou {tipo} {nome} ({datetime.datetime.now().strftime('%H:%M')})")
        messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")
        self.criar_menu_principal()

    def mostrar_produtos(self):
        self.limpar_quadro()
        self.quadro_produtos = ctk.CTkFrame(self)
        self.quadro_produtos.pack(pady=20)

        ctk.CTkLabel(self.quadro_produtos, text="Produtos").pack(pady=10)

        quadro_fisicos = ctk.CTkFrame(self.quadro_produtos)
        quadro_fisicos.pack(side=ctk.LEFT, padx=10)
        ctk.CTkLabel(quadro_fisicos, text="Pizzas").pack()
        for produto in fisicos:
            self.exibir_produto(quadro_fisicos, produto)

        quadro_liquidos = ctk.CTkFrame(self.quadro_produtos)
        quadro_liquidos.pack(side=ctk.LEFT, padx=10)
        ctk.CTkLabel(quadro_liquidos, text="Bebidas").pack()
        for produto in liquidos:
            self.exibir_produto(quadro_liquidos, produto)

        ctk.CTkButton(self.quadro_produtos, text="Voltar", command=self.criar_menu_principal).pack(pady=10)

    def editar_produto(self, produto):
        self.limpar_quadro()
        self.quadro_editar = ctk.CTkFrame(self)
        self.quadro_editar.pack(pady=20)

        ctk.CTkLabel(self.quadro_editar, text=f"Editar Produto - {produto.nome}").pack(pady=10)

        self.var_editar_imagem = ctk.StringVar(value=produto.imagem)
        ctk.CTkLabel(self.quadro_editar, text="Imagem").pack()
        ctk.CTkEntry(self.quadro_editar, textvariable=self.var_editar_imagem).pack()

        self.var_editar_nome = ctk.StringVar(value=produto.nome)
        ctk.CTkLabel(self.quadro_editar, text="Nome").pack()
        ctk.CTkEntry(self.quadro_editar, textvariable=self.var_editar_nome).pack()

        self.var_editar_ingredientes = ctk.StringVar(value=getattr(produto, 'ingredientes', ''))
        ctk.CTkLabel(self.quadro_editar, text="Ingredientes (somente para Pizzas)").pack()
        ctk.CTkEntry(self.quadro_editar, textvariable=self.var_editar_ingredientes).pack()

        self.var_editar_peso = ctk.StringVar(value=getattr(produto, 'peso', ''))
        ctk.CTkLabel(self.quadro_editar, text="Peso (somente para Pizzas)").pack()
        ctk.CTkEntry(self.quadro_editar, textvariable=self.var_editar_peso).pack()

        self.var_editar_volume = ctk.StringVar(value=getattr(produto, 'volume', ''))
        ctk.CTkLabel(self.quadro_editar, text="Volume (somente para Bebidas)").pack()
        ctk.CTkEntry(self.quadro_editar, textvariable=self.var_editar_volume).pack()

        self.var_editar_preco = ctk.StringVar(value=produto.preco)
        ctk.CTkLabel(self.quadro_editar, text="Preço").pack()
        ctk.CTkEntry(self.quadro_editar, textvariable=self.var_editar_preco).pack()

        self.var_editar_acompanhamento = ctk.StringVar(value=produto.acompanhamento)
        ctk.CTkLabel(self.quadro_editar, text="Acompanhamento").pack()
        ctk.CTkEntry(self.quadro_editar, textvariable=self.var_editar_acompanhamento).pack()

        ctk.CTkButton(self.quadro_editar, text="Salvar", command=lambda: self.salvar_edicao(produto)).pack(pady=10)
        ctk.CTkButton(self.quadro_editar, text="Cancelar", command=self.criar_menu_principal).pack(pady=10)

    def salvar_edicao(self, produto):
        produto.imagem = self.var_editar_imagem.get()
        produto.nome = self.var_editar_nome.get()
        produto.ingredientes = self.var_editar_ingredientes.get()
        produto.peso = self.var_editar_peso.get()
        produto.volume = self.var_editar_volume.get()
        produto.preco = self.var_editar_preco.get()
        produto.acompanhamento = self.var_editar_acompanhamento.get()

        salvar_produtos()
        self.log_atividades.append(f"{self.nome_usuario} editou {produto.nome} ({datetime.datetime.now().strftime('%H:%M')})")
        messagebox.showinfo("Sucesso", "Produto editado com sucesso!")
        self.criar_menu_principal()

    def atualizar_sugestoes_pesquisa(self, *args):
        query = self.var_pesquisa.get().lower()
        sugestoes = [produto for produto in fisicos + liquidos if query in produto.nome.lower()]
        self.lista_sugestoes.delete(0, 'end')
        for sugestao in sugestoes:
            self.lista_sugestoes.insert('end', sugestao.nome)

    def selecionar_sugestao(self, event):
        if self.lista_sugestoes.curselection():
            index = self.lista_sugestoes.curselection()[0]
            nome_produto = self.lista_sugestoes.get(index)
            for produto in fisicos + liquidos:
                if produto.nome == nome_produto:
                    self.editar_produto(produto)
                    break

    def criar_botao_retorno(self, parent, comando):
        ctk.CTkButton(parent, text="Voltar", command=comando).pack(pady=10)

if __name__ == "__main__":
    app = Aplicativo()
    app.mainloop()
