import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

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

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento de Produtos")
        self.geometry("800x600")
        self.nome_usuario = None
        self.create_login_screen()

    def create_login_screen(self):
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="E-mail").pack()
        self.email_entry = tk.Entry(self.login_frame)
        self.email_entry.pack()

        tk.Label(self.login_frame, text="Nome").pack()
        self.nome_entry = tk.Entry(self.login_frame)
        self.nome_entry.pack()

        tk.Label(self.login_frame, text="Senha").pack()
        self.senha_entry = tk.Entry(self.login_frame, show="*")
        self.senha_entry.pack()

        tk.Label(self.login_frame, text="Confirme a Senha").pack()
        self.conf_senha_entry = tk.Entry(self.login_frame, show="*")
        self.conf_senha_entry.pack()

        tk.Button(self.login_frame, text="Login", command=self.verificar_credenciais).pack(pady=10)

    def verificar_credenciais(self):
        email = self.email_entry.get()
        nome = self.nome_entry.get()
        senha = self.senha_entry.get()
        confirmar_senha = self.conf_senha_entry.get()

        if senha == "PizzaBoa" and senha == confirmar_senha:
            self.nome_usuario = nome
            messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {nome}!")
            self.login_frame.destroy()
            self.create_main_menu()
        else:
            messagebox.showerror("Erro de Login", "Senha incorreta. Tente novamente.")

    def create_main_menu(self):
        self.clear_frame()

        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack(pady=20)

        tk.Label(self.menu_frame, text=f"{self.nome_usuario} - Menu Principal", font=("Helvetica", 16)).pack(pady=10)

        search_and_return_frame = tk.Frame(self.menu_frame)
        search_and_return_frame.pack(fill=tk.X)

        self.create_return_button(search_and_return_frame, self.create_main_menu)
        self.create_search_bar(search_and_return_frame)

        left_frame = tk.Frame(self.menu_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        right_frame = tk.Frame(self.menu_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        tk.Button(right_frame, text="+Criar", command=self.show_criar_menu).pack(pady=5)
        tk.Button(right_frame, text="Estoque", command=self.mostrar_produtos).pack(pady=5)
        tk.Button(right_frame, text="Menu", command=self.mostrar_produtos).pack(pady=5)
        tk.Button(right_frame, text="Editar", command=self.editar_produtos).pack(pady=5)

        self.create_product_display(left_frame, "Pizzas", fisicos)
        self.create_product_display(left_frame, "Bebidas", liquidos)
        self.create_product_display(left_frame, "Acompanhamentos", acompanhamentos)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def create_product_display(self, parent, title, products):
        frame = tk.Frame(parent)
        frame.pack(pady=10, fill='x')
        tk.Label(frame, text=title, font=("Helvetica", 14)).pack(anchor='w')
        display_frame = tk.Frame(frame)
        display_frame.pack()
        for product in products[-3:]:
            self.display_product(display_frame, product)

    def display_product(self, parent, product):
        product_frame = tk.Frame(parent, width=50, height=50, relief=tk.RAISED, borderwidth=1)
        product_frame.pack_propagate(False)
        product_frame.pack(side=tk.LEFT, padx=5)

        img_label = tk.Label(product_frame, text=product.imagem, width=30, height=30)
        img_label.pack()
        name_label = tk.Label(product_frame, text=product.nome, wraplength=50)
        name_label.pack()
        product_frame.bind("<Button-1>", lambda e: self.editar_produto(product))

    def create_search_bar(self, parent):
        search_frame = tk.Frame(parent)
        search_frame.pack(side=tk.RIGHT)
        tk.Label(search_frame, text="Pesquisar: ").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT)
        self.search_var.trace("w", self.update_search_suggestions)
        self.suggestion_listbox = tk.Listbox(search_frame)
        self.suggestion_listbox.pack(side=tk.LEFT)
        self.suggestion_listbox.bind("<<ListboxSelect>>", self.on_suggestion_select)

    def update_search_suggestions(self, *args):
        search_term = self.search_var.get().lower()
        self.suggestion_listbox.delete(0, tk.END)
        suggestions = [prod.nome for prod in fisicos + liquidos + acompanhamentos if search_term in prod.nome.lower()]
        for suggestion in suggestions:
            self.suggestion_listbox.insert(tk.END, suggestion)

    def on_suggestion_select(self, event):
        selected_index = self.suggestion_listbox.curselection()
        if selected_index:
            selected_name = self.suggestion_listbox.get(selected_index)
            for product in fisicos + liquidos + acompanhamentos:
                if product.nome == selected_name:
                    self.editar_produto(product)
                    break

    def create_return_button(self, parent, command):
        return_button = tk.Button(parent, text="Voltar ao Menu Principal", command=self.create_main_menu)
        return_button.pack(side=tk.LEFT, padx=5)

    def show_criar_menu(self):
        self.clear_frame()
        self.criar_frame = tk.Frame(self)
        self.criar_frame.pack(pady=20)

        tk.Label(self.criar_frame, text="Criar", font=("Helvetica", 16)).pack(pady=10)
        search_and_return_frame = tk.Frame(self.criar_frame)
        search_and_return_frame.pack(fill=tk.X)
        self.create_return_button(search_and_return_frame, self.create_main_menu)
        self.create_search_bar(search_and_return_frame)
        
        tk.Button(self.criar_frame, text="Criar Físicos", command=self.criarfisicos).pack(pady=5)
        tk.Button(self.criar_frame, text="Criar Líquidos", command=self.criarliquidos).pack(pady=5)
    
    def criarfisicos(self):
        imagem = simpledialog.askstring("Criar Físicos", "Imagem:")
        nome = simpledialog.askstring("Criar Físicos", "Nome:")
        ingredientes = simpledialog.askstring("Criar Físicos", "Ingredientes:")
        peso = float(simpledialog.askstring("Criar Físicos", "Peso:"))
        preco = float(simpledialog.askstring("Criar Físicos", "Preço:"))
        acompanhamento = simpledialog.askstring("Criar Físicos", "Acompanhamento (Sim/Não):")
        
        novo_fisico = Fisicos(imagem, nome, ingredientes, peso, preco, acompanhamento)
        fisicos.append(novo_fisico)
        if acompanhamento.lower() == "sim":
            acompanhamentos.append(novo_fisico)
        messagebox.showinfo("Criar Físicos", "Produto Físico Criado!")
        self.create_main_menu()

    def criarliquidos(self):
        imagem = simpledialog.askstring("Criar Líquidos", "Imagem:")
        nome = simpledialog.askstring("Criar Líquidos", "Nome:")
        volume = float(simpledialog.askstring("Criar Líquidos", "Volume:"))
        preco = float(simpledialog.askstring("Criar Líquidos", "Preço:"))
        acompanhamento = simpledialog.askstring("Criar Líquidos", "Acompanhamento (Sim/Não):")
        
        novo_liquido = Liquidos(imagem, nome, volume, preco, acompanhamento)
        liquidos.append(novo_liquido)
        if acompanhamento.lower() == "sim":
            acompanhamentos.append(novo_liquido)
        messagebox.showinfo("Criar Líquidos", "Produto Líquido Criado!")
        self.create_main_menu()

    def mostrar_produtos(self):
        self.clear_frame()
        self.produtos_frame = tk.Frame(self)
        self.produtos_frame.pack(pady=20)

        tk.Label(self.produtos_frame, text="Produtos em Estoque", font=("Helvetica", 16)).pack(pady=10)
        search_and_return_frame = tk.Frame(self.produtos_frame)
        search_and_return_frame.pack(fill=tk.X)
        self.create_return_button(search_and_return_frame, self.create_main_menu)
        self.create_search_bar(search_and_return_frame)

        tk.Label(self.produtos_frame, text="Produtos Físicos:").pack()
        for f in fisicos:
            tk.Label(self.produtos_frame, text=f"Nome: {f.nome}, Preço: {f.preco}").pack()

        tk.Label(self.produtos_frame, text="Produtos Líquidos:").pack()
        for l in liquidos:
            tk.Label(self.produtos_frame, text=f"Nome: {l.nome}, Preço: {l.preco}").pack()

        tk.Label(self.produtos_frame, text="Acompanhamentos:").pack()
        for a in acompanhamentos:
            tk.Label(self.produtos_frame, text=f"Nome: {a.nome}, Preço: {a.preco}").pack()

    def editar_produtos(self):
        self.clear_frame()
        self.editar_frame = tk.Frame(self)
        self.editar_frame.pack(pady=20)
        
        tk.Label(self.editar_frame, text="Editar Produtos", font=("Helvetica", 16)).pack(pady=10)
        search_and_return_frame = tk.Frame(self.editar_frame)
        search_and_return_frame.pack(fill=tk.X)
        self.create_return_button(search_and_return_frame, self.create_main_menu)
        self.create_search_bar(search_and_return_frame)

        tk.Label(self.editar_frame, text="Produtos Físicos:").pack()
        for f in sorted(fisicos, key=lambda x: x.nome):
            tk.Button(self.editar_frame, text=f.nome, command=lambda f=f: self.editar_produto(f)).pack()

        tk.Label(self.editar_frame, text="Produtos Líquidos:").pack()
        for l in sorted(liquidos, key=lambda x: x.nome):
            tk.Button(self.editar_frame, text=l.nome, command=lambda l=l: self.editar_produto(l)).pack()

        tk.Label(self.editar_frame, text="Acompanhamentos:").pack()
        for a in sorted(acompanhamentos, key=lambda x: x.nome):
            tk.Button(self.editar_frame, text=a.nome, command=lambda a=a: self.editar_produto(a)).pack()

    def editar_produto(self, produto):
        self.clear_frame()
        self.edit_frame = tk.Frame(self)
        self.edit_frame.pack(pady=20)
        
        tk.Label(self.edit_frame, text=f"Editar {produto.nome}", font=("Helvetica", 16)).pack(pady=10)
        search_and_return_frame = tk.Frame(self.edit_frame)
        search_and_return_frame.pack(fill=tk.X)
        self.create_return_button(search_and_return_frame, self.editar_produtos)
        self.create_search_bar(search_and_return_frame)

        img_label = tk.Label(self.edit_frame, text=f"Imagem: {produto.imagem}")
        img_label.pack()
        self.img_entry = tk.Entry(self.edit_frame)
        self.img_entry.insert(0, produto.imagem)
        self.img_entry.pack()

        name_label = tk.Label(self.edit_frame, text=f"Nome: {produto.nome}")
        name_label.pack()
        self.name_entry = tk.Entry(self.edit_frame)
        self.name_entry.insert(0, produto.nome)
        self.name_entry.pack()

        if isinstance(produto, Fisicos):
            ing_label = tk.Label(self.edit_frame, text=f"Ingredientes: {produto.ingredientes}")
            ing_label.pack()
            self.ing_entry = tk.Entry(self.edit_frame)
            self.ing_entry.insert(0, produto.ingredientes)
            self.ing_entry.pack()

            weight_label = tk.Label(self.edit_frame, text=f"Peso: {produto.peso}")
            weight_label.pack()
            self.weight_entry = tk.Entry(self.edit_frame)
            self.weight_entry.insert(0, produto.peso)
            self.weight_entry.pack()

        elif isinstance(produto, Liquidos):
            volume_label = tk.Label(self.edit_frame, text=f"Volume: {produto.volume}")
            volume_label.pack()
            self.volume_entry = tk.Entry(self.edit_frame)
            self.volume_entry.insert(0, produto.volume)
            self.volume_entry.pack()

        price_label = tk.Label(self.edit_frame, text=f"Preço: {produto.preco}")
        price_label.pack()
        self.price_entry = tk.Entry(self.edit_frame)
        self.price_entry.insert(0, produto.preco)
        self.price_entry.pack()

        acomp_label = tk.Label(self.edit_frame, text=f"Acompanhamento: {produto.acompanhamento}")
        acomp_label.pack()
        self.acomp_entry = tk.Entry(self.edit_frame)
        self.acomp_entry.insert(0, produto.acompanhamento)
        self.acomp_entry.pack()

        tk.Button(self.edit_frame, text="Salvar", command=lambda: self.salvar_edicao(produto)).pack(pady=5)
        tk.Button(self.edit_frame, text="Excluir", command=lambda: self.excluir_produto(produto)).pack(pady=5)

    def salvar_edicao(self, produto):
        produto.imagem = self.img_entry.get()
        produto.nome = self.name_entry.get()

        if isinstance(produto, Fisicos):
            produto.ingredientes = self.ing_entry.get()
            produto.peso = float(self.weight_entry.get())

        elif isinstance(produto, Liquidos):
            produto.volume = float(self.volume_entry.get())

        produto.preco = float(self.price_entry.get())
        acompanhamento = self.acomp_entry.get()

        if acompanhamento.lower() == "sim" and produto not in acompanhamentos:
            acompanhamentos.append(produto)
        elif acompanhamento.lower() == "não" and produto in acompanhamentos:
            acompanhamentos.remove(produto)
        produto.acompanhamento = acompanhamento

        messagebox.showinfo("Editar Produto", "Produto atualizado!")
        self.create_main_menu()

    def excluir_produto(self, produto):
        if isinstance(produto, Fisicos):
            fisicos.remove(produto)
        elif isinstance(produto, Liquidos):
            liquidos.remove(produto)
        if produto in acompanhamentos:
            acompanhamentos.remove(produto)
        messagebox.showinfo("Excluir Produto", "Produto excluído!")
        self.create_main_menu()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
