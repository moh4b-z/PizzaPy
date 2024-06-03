import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

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

def registrar_alteracoes(usuario, alteracoes):
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('alterações.txt', 'a', encoding='utf-8') as arquivo:
        arquivo.write(f"Usuário: {usuario}\n")
        arquivo.write(f"Hora de login: {hora}\n")
        arquivo.write("Alterações:\n")
        for alteracao in alteracoes:
            arquivo.write(alteracao + "\n")
        arquivo.write(f"Hora de fechar a tela: {hora}\n\n")

def enviar_email(usuario, alteracoes):
    email_do_usuario = "pizzaboasenai127@gmail.com"  # Insira seu email aqui
    senha = "senai127"  # Insira sua senha aqui
    destinatario = "pizzaboasenai127@gmail.com"  # Insira o email do destinatário aqui

    servidor_smtp = "smtp.gmail.com"
    porta_smtp = 587

    mensagem = MIMEMultipart()
    mensagem['From'] = email_do_usuario
    mensagem['To'] = destinatario
    mensagem['Subject'] = "Alterações no sistema"

    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    corpo_email = f"Usuário: {usuario}\n"
    corpo_email += f"Hora de login: {hora}\n"
    corpo_email += "Alterações:\n"
    for alteracao in alteracoes:
        corpo_email += alteracao + "\n"
    corpo_email += f"Hora de fechar a tela: {hora}\n"

    mensagem.attach(MIMEText(corpo_email, 'plain'))

    try:
        servidor = smtplib.SMTP(servidor_smtp, porta_smtp)
        servidor.starttls()
        servidor.login(email_do_usuario, senha)
        texto = mensagem.as_string()
        servidor.sendmail(email_do_usuario, destinatario, texto)
        servidor.quit()
        messagebox.showinfo("Email enviado", "As alterações foram enviadas por email com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro ao enviar email", f"Ocorreu um erro ao enviar o email: {str(e)}")

class Aplicacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento de Produtos")
        self.geometry("800x600")
        self.nome_usuario = None
        carregar_produtos()
        self.criar_tela_login()

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
        quadro = tk.Frame(parent)
        quadro.pack(pady=10, fill='x')
        tk.Label(quadro, text=titulo, font=("Helvetica", 14)).pack(anchor='w')
        quadro_exibicao = tk.Frame(quadro)
        quadro_exibicao.pack()
        for produto in produtos[-3:]:
            self.exibir_produto(quadro_exibicao, produto)

    def exibir_produto(self, parent, produto):
        quadro_produto = tk.Frame(parent, width=50, height=50, relief=tk.RAISED, borderwidth=1)
        quadro_produto.pack_propagate(False)
        quadro_produto.pack(side=tk.LEFT, padx=5)

        rotulo_imagem = tk.Label(quadro_produto, text=produto.imagem, width=30, height=30)
        rotulo_imagem.pack()
        rotulo_nome = tk.Label(quadro_produto, text=produto.nome, wraplength=50)
        rotulo_nome.pack()
        quadro_produto.bind("<Button-1>", lambda e: self.editar_produto(produto))

    def criar_barra_pesquisa(self, parent):
        quadro_pesquisa = tk.Frame(parent)
        quadro_pesquisa.pack(side=tk.RIGHT)
        tk.Label(quadro_pesquisa, text="Pesquisar: ").pack(side=tk.LEFT)
        self.var_pesquisa = tk.StringVar()
        self.entrada_pesquisa = tk.Entry(quadro_pesquisa, textvariable=self.var_pesquisa)
        self.entrada_pesquisa.pack(side=tk.LEFT)
        self.var_pesquisa.trace("w", self.atualizar_sugestoes_pesquisa)
        self.lista_sugestoes = tk.Listbox(quadro_pesquisa)
        self.lista_sugestoes.pack(side=tk.LEFT)
        self.lista_sugestoes.bind("<<ListboxSelect>>", self.selecionar_sugestao)

    def atualizar_sugestoes_pesquisa(self, *args):
        termo_pesquisa = self.var_pesquisa.get().lower()
        self.lista_sugestoes.delete(0, tk.END)
        sugestoes = [prod.nome for prod in fisicos + liquidos + acompanhamentos if termo_pesquisa in prod.nome.lower()]
        for sugestao in sugestoes:
            self.lista_sugestoes.insert(tk.END, sugestao)

    def selecionar_sugestao(self, event):
        indice_selecionado = self.lista_sugestoes.curselection()
        if indice_selecionado:
            nome_selecionado = self.lista_sugestoes.get(indice_selecionado)
            for produto in fisicos + liquidos + acompanhamentos:
                if produto.nome == nome_selecionado:
                    self.editar_produto(produto)
                    break

    def criar_botao_retorno(self, parent, comando):
        botao_retorno = tk.Button(parent, text="Voltar ao Menu Principal", command=self.criar_menu_principal)
        botao_retorno.pack(side=tk.LEFT, padx=5)

    def mostrar_menu_criar(self):
        self.limpar_quadro()
        self.quadro_criar = tk.Frame(self)
        self.quadro_criar.pack(pady=20)

        tk.Label(self.quadro_criar, text="Menu de Criação de Produtos", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(self.quadro_criar, text="Criar Produto Físico", command=self.criar_produto_fisico).pack(pady=5)
        tk.Button(self.quadro_criar, text="Criar Produto Líquido", command=self.criar_produto_liquido).pack(pady=5)

    def criar_produto_fisico(self):
        nome = simpledialog.askstring("Nome", "Digite o nome do produto:")
        ingredientes = simpledialog.askstring("Ingredientes", "Digite os ingredientes do produto:")
        peso = simpledialog.askfloat("Peso", "Digite o peso do produto em gramas:")
        preco = simpledialog.askfloat("Preço", "Digite o preço do produto:")
        acompanha = simpledialog.askstring("Acompanha", "O produto acompanha algo? (sim/não)").lower()

        produto = Fisicos("imagem.jpg", nome, ingredientes, peso, preco, acompanha)
        fisicos.append(produto)
        if acompanha == "sim":
            acompanhamentos.append(produto)
        salvar_produtos()
        messagebox.showinfo("Produto Criado", "O produto foi criado com sucesso.")

    def criar_produto_liquido(self):
        nome = simpledialog.askstring("Nome", "Digite o nome do produto:")
        volume = simpledialog.askfloat("Volume", "Digite o volume do produto em ml:")
        preco = simpledialog.askfloat("Preço", "Digite o preço do produto:")
        acompanha = simpledialog.askstring("Acompanha", "O produto acompanha algo? (sim/não)").lower()

        produto = Liquidos("imagem.jpg", nome, volume, preco, acompanha)
        liquidos.append(produto)
        if acompanha == "sim":
            acompanhamentos.append(produto)
        salvar_produtos()
        messagebox.showinfo("Produto Criado", "O produto foi criado com sucesso.")

    def editar_produto(self, produto):
        pass

    def mostrar_produtos(self):
        pass

    def editar_produtos(self):
        pass

if __name__ == "__main__":
    app = Aplicacao()
    app.mainloop()
