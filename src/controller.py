import model
import tkinter as tk
from tkinter import messagebox

class LivroController:
    def __init__(self):
        self.titulos = []
        self.paginaatual = 0
        self.itenspagina = 10
        self.filtroletra = "Todos"
        self.filtrobusca = ""

    def carregar_titulos(self):
        self.titulos = model.listar_livros()
        lista = []
        for c in range(len(self.titulos)):
            titulo = self.titulos[c][1]
            lista.append(titulo)
        return lista

    def selecionar_primeiro(self):
        if self.titulos:
            return self.titulos[0][1]
        return ""

    def buscar_dados_detalhes(self):
        offset = self.paginaatual * self.itenspagina
        return model.buscar_detalhes(
            offset,
            self.itenspagina,
            self.filtroletra,
            self.filtrobusca
        )

    def avancar_pagina(self):
        self.paginaatual += 1

    def voltar_pagina(self):
        if self.paginaatual > 0:
            self.paginaatual -= 1

    def resetar_paginacao(self):
        self.paginaatual = 0

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
