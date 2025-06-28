import model
import tkinter as tk
from tkinter import messagebox

class LivroController:
    def __init__(self):
        self.titulos = []
        self.pagina_atual = 0
        self.itens_por_pagina = 10
        self.filtro_letra = "Todos"
        self.filtro_busca = ""

    def carregar_titulos(self):
        self.titulos = model.listar_livros()
        return [titulo for _, titulo in self.titulos]

    def selecionar_primeiro(self):
        return self.titulos[0][1] if self.titulos else ""

    def buscar_dados_detalhes(self):
        offset = self.pagina_atual * self.itens_por_pagina
        return model.buscar_detalhes(
            offset,
            self.itens_por_pagina,
            self.filtro_letra,
            self.filtro_busca
        )

    def avancar_pagina(self):
        self.pagina_atual += 1

    def voltar_pagina(self):
        if self.pagina_atual > 0:
            self.pagina_atual -= 1

    def resetar_paginacao(self):
        self.pagina_atual = 0

def selecionar_banco(view_ref):
    def selecionar(opcao):
        if opcao == "sqlite":
            model.usar_sqlite()
            model.inicializar_sqlite_se_necessario()
        else:
            model.usar_postgres()
        view_ref.carregar_titulos()
        modal.destroy()

    modal = tk.Toplevel()
    modal.title("Selecionar banco")
    modal.geometry("300x120")

    tk.Label(modal, text="Escolha o banco de dados desejado").pack(pady=10)
    tk.Button(modal, text="SQLite", width=20, command=lambda: selecionar("sqlite")).pack(pady=5)
    tk.Button(modal, text="PostgreSQL", width=20, command=lambda: selecionar("postgres")).pack(pady=5)
