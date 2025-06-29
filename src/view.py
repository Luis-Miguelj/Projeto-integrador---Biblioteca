import tkinter as tk
from tkinter import ttk, messagebox
from controller import LivroController, selecionar_banco
import string

class LivroView:
    def __init__(self, root):
        self.ctrl = LivroController()
        self.root = root
        self.root.title("TDD: teste com combobox e jtable")
        self.root.geometry("550x200")

        self.combo_titulos = None
        self.entry_busca = None
        self.combo_letra = None
        self.tree = None

        self.build_main_interface()

    def build_main_interface(self):
        frame_topo = tk.Frame(self.root)
        frame_topo.pack(pady=10)

        tk.Label(frame_topo, text="Livro").pack(side=tk.LEFT, padx=5)
        self.combo_titulos = ttk.Combobox(frame_topo, width=35, state="readonly")
        self.combo_titulos.pack(side=tk.LEFT)
        tk.Button(frame_topo, text="Carregar", command=lambda: selecionar_banco(self)).pack(side=tk.LEFT, padx=5)

        frame_meio = tk.Frame(self.root)
        frame_meio.pack(pady=10)

        tk.Label(frame_meio, text="Dados dos livros").pack(side=tk.LEFT, padx=5)
        tk.Button(frame_meio, text="Carregar", width=35, command=self.abrir_detalhes).pack(side=tk.LEFT, padx=5)

        frame_rodape = tk.Frame(self.root)
        frame_rodape.pack(pady=10)

        tk.Button(frame_rodape, text="Fechar", width=50, command=self.root.destroy).pack()

    def carregar_titulos(self):
        titulos = self.ctrl.carregar_titulos()
        self.combo_titulos['values'] = titulos
        if titulos:
            self.combo_titulos.set(self.ctrl.selecionar_primeiro())
        messagebox.showinfo("Info", f"Carregados {len(titulos)} registros.")

    def abrir_detalhes(self):
        nova = tk.Toplevel()
        nova.title("Livros com Filtros")
        nova.geometry("900x550")

        frame_filtros = tk.Frame(nova)
        frame_filtros.pack(pady=10)

        tk.Label(frame_filtros, text="Filtrar por letra:").pack(side=tk.LEFT)
        letras = ["Todos"] + list(string.ascii_uppercase)
        self.combo_letra = ttk.Combobox(frame_filtros, values=letras, state="readonly", width=6)
        self.combo_letra.set("Todos")
        self.combo_letra.pack(side=tk.LEFT, padx=5)
        self.combo_letra.bind("<<ComboboxSelected>>", lambda e: self.aplicar_filtros())

        tk.Label(frame_filtros, text="Buscar:").pack(side=tk.LEFT, padx=5)
        self.entry_busca = tk.Entry(frame_filtros, width=30)
        self.entry_busca.pack(side=tk.LEFT)
        tk.Button(frame_filtros, text="Pesquisar", command=self.aplicar_filtros).pack(side=tk.LEFT, padx=5)

        colunas = ("ID", "Título", "Edição", "Ano", "Autor")
        self.tree = ttk.Treeview(nova, columns=colunas, show="headings")
        for col in colunas:
            self.tree.heading(col, text=col)
            if col != "Título":
                self.tree.column(col, width=130)
            else:
                self.tree.column(col, width=200)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree.bind("<Double-1>", lambda event: self.mostrar_detalhes(nova))

        frame_nav = tk.Frame(nova)
        frame_nav.pack(pady=10)

        tk.Button(frame_nav, text="Anterior", command=self.pagina_anterior).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_nav, text="Próxima", command=self.pagina_proxima).pack(side=tk.LEFT, padx=5)

        self.atualizar_tabela()
    
    def mostrar_detalhes(self, janela):
        item = self.tree.selection()
        if not item:
            return

        valores = self.tree.item(item[0], "values")

        # Fecha a janela atual
        janela.destroy()

        # Mostra um alerta com os detalhes
        mensagem = f"""Código: {valores[0]}\nTítulo: {valores[1]}\nEdição: {valores[2]}\nAno: {valores[3]}\nAutor: {valores[4]}""".strip()

        messagebox.showinfo("Detalhes do Livro", mensagem)

    def aplicar_filtros(self):
        self.ctrl.filtroletra = self.combo_letra.get()
        self.ctrl.filtrobusca = self.entry_busca.get().strip()
        self.ctrl.resetar_paginacao()
        self.atualizar_tabela()

    def atualizar_tabela(self):
        dados = self.ctrl.buscar_dados_detalhes()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for linha in dados:
            self.tree.insert("", tk.END, values=linha)

    def pagina_proxima(self):
        self.ctrl.avancar_pagina()
        self.atualizar_tabela()

    def pagina_anterior(self):
        self.ctrl.voltar_pagina()
        self.atualizar_tabela()