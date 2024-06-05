import customtkinter as ctk
from tkinter import PhotoImage, messagebox
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configuracoes_da_janela_inicial()
        self.tela_de_login()

    # Configurando a janela principal
    def configuracoes_da_janela_inicial(self):
        self.geometry("700x400")
        self.title("Login")
        self.resizable(False, False)

    def tela_de_login(self):
        
        
        image_path = os.path.abspath("foto_login.png")
        if os.path.isfile(image_path):
            try:
                self.img = PhotoImage(file=image_path)
                self.lb_img = ctk.CTkLabel(self, text="", image=self.img)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar a imagem: {e}")
                self.lb_img = ctk.CTkLabel(self, text="Imagem não encontrada", font=("Century Gothic bold", 14))
        else:
            messagebox.showerror("Erro", f"Arquivo {image_path} não encontrado.")
            self.lb_img = ctk.CTkLabel(self, text="Imagem não encontrada", font=("Century Gothic bold", 14))

        self.lb_img.grid(row=1, column=0, padx=10)

        # Título da nossa plataforma
        self.title_label = ctk.CTkLabel(self, text="Faça o seu login", font=("Century Gothic bold", 14))
        self.title_label.grid(row=0, column=0, pady=10, padx=10)

        # Criando o frame do formulário do login
        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=350, y=10)

        # Colocando widgets dentro do frame - formulário de login
        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça o seu Login", font=("Century Gothic bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        self.entrada_nome = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Seu nome de usuário...", font=("Century Gothic bold", 16), corner_radius=15, border_color="green")
        self.entrada_nome.grid(row=1, column=0, pady=10, padx=10)

        self.entrada_senha = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Sua senha...", font=("Century Gothic bold", 16), show="*", corner_radius=15, border_color="green")
        self.entrada_senha.grid(row=2, column=0, pady=10, padx=10)

        self.entrada_conf_senha = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Confirme sua senha...", font=("Century Gothic bold", 16), show="*", corner_radius=15, border_color="green")
        self.entrada_conf_senha.grid(row=3, column=0, pady=10, padx=10)

        self.ver_senha_var = ctk.IntVar()
        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text="Clique para ver a senha...", font=("Century Gothic bold", 14), variable=self.ver_senha_var, command=self.toggle_senha)
        self.ver_senha.grid(row=4, column=0, pady=10, padx=10)

        self.btn_login = ctk.CTkButton(self.frame_login, width=300, text="Fazer Login", font=("Century Gothic bold", 16), corner_radius=15, fg_color="green", command=self.verificar_credenciais)
        self.btn_login.grid(row=5, column=0, pady=10, padx=10)



    def criar_menu_principal(self):
        self.limpar_quadro()

        self.quadro_menu = tk.Frame(self)
        self.quadro_menu.pack(pady=20)

        
    def limpar_quadro(self):
        for widget in self.winfo_children():
            widget.pack_forget()

if __name__ == "__main__":
    app = App()
    app.mainloop()
