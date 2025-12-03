import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

class EstoqueView:
    """Interface gráfica do sistema de estoque"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sistema de Controle de Estoque")
        self.root.geometry("1200x700")
        
        # Callbacks para controller
        self.on_adicionar_produto: Callable = None
        self.on_entrada_insumo: Callable = None
        self.on_saida_insumo: Callable = None
        self.on_gerar_relatorio: Callable = None
        self.on_listar_produtos: Callable = None
        self.on_atualizar_alertas: Callable = None
        
        self._criar_interface()
    
    def _criar_interface(self):
        """Cria todos os componentes da interface"""
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Abas
        self.tab_produtos = ttk.Frame(self.notebook)
        self.tab_movimentacao = ttk.Frame(self.notebook)
        self.tab_relatorios = ttk.Frame(self.notebook)
        self.tab_alertas = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_produtos, text="📦 Produtos")
        self.notebook.add(self.tab_movimentacao, text="📊 Movimentação")
        self.notebook.add(self.tab_relatorios, text="📄 Relatórios")
        self.notebook.add(self.tab_alertas, text="⚠️ Alertas")
        
        self._criar_aba_produtos()
        self._criar_aba_movimentacao()
        self._criar_aba_relatorios()
        self._criar_aba_alertas()
    
    def _criar_aba_produtos(self):
        """Aba de cadastro e listagem de produtos"""
        
        # Frame de formulário
        frame_form = ttk.LabelFrame(self.tab_produtos, text="Cadastro de Produto", padding=15)
        frame_form.pack(fill='x', padx=10, pady=10)
        
        # Campos
        ttk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_nome = ttk.Entry(frame_form, width=40)
        self.entry_nome.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(frame_form, text="Descrição:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_descricao = ttk.Entry(frame_form, width=40)
        self.entry_descricao.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(frame_form, text="Qtd Mínima:").grid(row=0, column=2, sticky='w', pady=5, padx=(20,0))
        self.entry_qtd_minima = ttk.Entry(frame_form, width=15)
        self.entry_qtd_minima.grid(row=0, column=3, pady=5, padx=5)
        
        ttk.Label(frame_form, text="Preço Unit (R$):").grid(row=1, column=2, sticky='w', pady=5, padx=(20,0))
        self.entry_preco = ttk.Entry(frame_form, width=15)
        self.entry_preco.grid(row=1, column=3, pady=5, padx=5)
        
        # Botões
        frame_btns = ttk.Frame(frame_form)
        frame_btns.grid(row=2, column=0, columnspan=4, pady=15)
        
        ttk.Button(frame_btns, text="✅ Adicionar", 
                   command=self._handle_adicionar_produto).pack(side='left', padx=5)
        ttk.Button(frame_btns, text="🔄 Limpar", 
                   command=self._limpar_formulario_produto).pack(side='left', padx=5)
        
        # Frame de listagem
        frame_lista = ttk.LabelFrame(self.tab_produtos, text="Produtos Cadastrados", padding=15)
        frame_lista.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview
        colunas = ('ID', 'Nome', 'Descrição', 'Estoque', 'Mínimo', 'Preço')
        self.tree_produtos = ttk.Treeview(frame_lista, columns=colunas, show='headings', height=15)
        
        larguras = [50, 200, 300, 80, 80, 100]
        for col, largura in zip(colunas, larguras):
            self.tree_produtos.heading(col, text=col)
            self.tree_produtos.column(col, width=largura)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_produtos.yview)
        self.tree_produtos.configure(yscroll=scrollbar.set)
        
        self.tree_produtos.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Botão atualizar
        ttk.Button(frame_lista, text="🔄 Atualizar Lista", 
                   command=self._handle_listar_produtos).pack(pady=5)
    
    def _criar_aba_movimentacao(self):
        """Aba de entrada/saída de insumos"""
        
        # Frame de entrada
        frame_entrada = ttk.LabelFrame(self.tab_movimentacao, text="➕ Entrada de Insumos", padding=15)
        frame_entrada.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_entrada, text="ID Produto:").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_entrada_id = ttk.Entry(frame_entrada, width=15)
        self.entry_entrada_id.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(frame_entrada, text="Quantidade:").grid(row=0, column=2, sticky='w', pady=5, padx=(20,0))
        self.entry_entrada_qtd = ttk.Entry(frame_entrada, width=15)
        self.entry_entrada_qtd.grid(row=0, column=3, pady=5, padx=5)
        
        ttk.Label(frame_entrada, text="Observação:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_entrada_obs = ttk.Entry(frame_entrada, width=50)
        self.entry_entrada_obs.grid(row=1, column=1, columnspan=3, pady=5, padx=5, sticky='ew')
        
        ttk.Button(frame_entrada, text="✅ Registrar Entrada", 
                   command=self._handle_entrada).grid(row=2, column=0, columnspan=4, pady=10)
        
        # Frame de saída
        frame_saida = ttk.LabelFrame(self.tab_movimentacao, text="➖ Saída de Insumos", padding=15)
        frame_saida.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_saida, text="ID Produto:").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_saida_id = ttk.Entry(frame_saida, width=15)
        self.entry_saida_id.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(frame_saida, text="Quantidade:").grid(row=0, column=2, sticky='w', pady=5, padx=(20,0))
        self.entry_saida_qtd = ttk.Entry(frame_saida, width=15)
        self.entry_saida_qtd.grid(row=0, column=3, pady=5, padx=5)
        
        ttk.Label(frame_saida, text="Observação:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_saida_obs = ttk.Entry(frame_saida, width=50)
        self.entry_saida_obs.grid(row=1, column=1, columnspan=3, pady=5, padx=5, sticky='ew')
        
        ttk.Button(frame_saida, text="✅ Registrar Saída", 
                   command=self._handle_saida).grid(row=2, column=0, columnspan=4, pady=10)
    
    def _criar_aba_relatorios(self):
        """Aba de geração de relatórios"""
        
        frame_filtros = ttk.LabelFrame(self.tab_relatorios, text="Filtros de Relatório", padding=15)
        frame_filtros.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_filtros, text="Data Início (AAAA-MM-DD):").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_data_inicio = ttk.Entry(frame_filtros, width=20)
        self.entry_data_inicio.grid(row=0, column=1, pady=5, padx=5)
        self.entry_data_inicio.insert(0, "AAAA-MM-DD")
        
        ttk.Label(frame_filtros, text="Data Fim (AAAA-MM-DD):").grid(row=0, column=2, sticky='w', pady=5, padx=(20,0))
        self.entry_data_fim = ttk.Entry(frame_filtros, width=20)
        self.entry_data_fim.grid(row=0, column=3, pady=5, padx=5)
        self.entry_data_fim.insert(0, "AAAA-MM-DD")
        
        ttk.Button(frame_filtros, text="📊 Gerar Relatório", 
                   command=self._handle_gerar_relatorio).grid(row=1, column=0, columnspan=4, pady=10)
        
        # Área de resultados
        frame_resultado = ttk.LabelFrame(self.tab_relatorios, text="Resultado", padding=15)
        frame_resultado.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.text_relatorio = tk.Text(frame_resultado, height=20, wrap='word', font=('Courier', 9))
        scrollbar_rel = ttk.Scrollbar(frame_resultado, orient='vertical', 
                                      command=self.text_relatorio.yview)
        self.text_relatorio.configure(yscroll=scrollbar_rel.set)
        
        self.text_relatorio.pack(side='left', fill='both', expand=True)
        scrollbar_rel.pack(side='right', fill='y')
    
    def _criar_aba_alertas(self):
        """Aba de alertas de estoque baixo"""
        
        frame_alertas = ttk.LabelFrame(self.tab_alertas, text="⚠️ Produtos Críticos", padding=15)
        frame_alertas.pack(fill='both', expand=True, padx=10, pady=10)
        
        colunas_alert = ('Status', 'ID', 'Produto', 'Estoque', 'Mínimo', 'Déficit')
        self.tree_alertas = ttk.Treeview(frame_alertas, columns=colunas_alert, 
                                         show='headings', height=15)
        
        larguras_alert = [100, 50, 250, 80, 80, 80]
        for col, largura in zip(colunas_alert, larguras_alert):
            self.tree_alertas.heading(col, text=col)
            self.tree_alertas.column(col, width=largura)
        
        scrollbar_alert = ttk.Scrollbar(frame_alertas, orient='vertical', 
                                        command=self.tree_alertas.yview)
        self.tree_alertas.configure(yscroll=scrollbar_alert.set)
        
        self.tree_alertas.pack(side='left', fill='both', expand=True)
        scrollbar_alert.pack(side='right', fill='y')
        
        ttk.Button(frame_alertas, text="🔄 Atualizar Alertas", 
                   command=self._handle_atualizar_alertas).pack(pady=5)
    
    # Handlers
    def _handle_adicionar_produto(self):
        if self.on_adicionar_produto:
            dados = {
                'nome': self.entry_nome.get(),
                'descricao': self.entry_descricao.get(),
                'qtd_minima': self.entry_qtd_minima.get(),
                'preco': self.entry_preco.get()
            }
            self.on_adicionar_produto(dados)
    
    def _handle_entrada(self):
        if self.on_entrada_insumo:
            dados = {
                'id_produto': self.entry_entrada_id.get(),
                'quantidade': self.entry_entrada_qtd.get(),
                'observacao': self.entry_entrada_obs.get()
            }
            self.on_entrada_insumo(dados)
    
    def _handle_saida(self):
        if self.on_saida_insumo:
            dados = {
                'id_produto': self.entry_saida_id.get(),
                'quantidade': self.entry_saida_qtd.get(),
                'observacao': self.entry_saida_obs.get()
            }
            self.on_saida_insumo(dados)
    
    def _handle_gerar_relatorio(self):
        if self.on_gerar_relatorio:
            filtros = {
                'data_inicio': self.entry_data_inicio.get(),
                'data_fim': self.entry_data_fim.get()
            }
            self.on_gerar_relatorio(filtros)
    
    def _handle_listar_produtos(self):
        if self.on_listar_produtos:
            self.on_listar_produtos()
    
    def _handle_atualizar_alertas(self):
        if self.on_atualizar_alertas:
            self.on_atualizar_alertas()
    
    def _limpar_formulario_produto(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.entry_qtd_minima.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
    
    # Métodos de atualização de dados
    def atualizar_lista_produtos(self, produtos: list):
        """Atualiza a Treeview de produtos"""
        self.tree_produtos.delete(*self.tree_produtos.get_children())
        for p in produtos:
            self.tree_produtos.insert('', 'end', values=(
                p['id_produto'], 
                p['nome_produto'], 
                p['descricao'],
                p['qtd_estoque'], 
                p['qtd_minima'], 
                f"R$ {p['preco_unitario']:.2f}"
            ))
    
    def atualizar_alertas(self, produtos_criticos: list):
        """Atualiza alertas de estoque crítico"""
        self.tree_alertas.delete(*self.tree_alertas.get_children())
        for p in produtos_criticos:
            percentual = (p['qtd_estoque'] / p['qtd_minima']) * 100 if p['qtd_minima'] > 0 else 0
            status = "🔴 CRÍTICO" if percentual < 50 else "🟡 ATENÇÃO"
            self.tree_alertas.insert('', 'end', values=(
                status, 
                p['id_produto'], 
                p['nome_produto'],
                p['qtd_estoque'], 
                p['qtd_minima'], 
                p['deficit']
            ))
    
    def exibir_relatorio(self, texto_relatorio: str):
        """Exibe relatório na área de texto"""
        self.text_relatorio.delete('1.0', tk.END)
        self.text_relatorio.insert('1.0', texto_relatorio)
    
    def mostrar_mensagem(self, titulo: str, mensagem: str, tipo: str = "info"):
        """Exibe mensagem para o usuário"""
        if tipo == "info":
            messagebox.showinfo(titulo, mensagem)
        elif tipo == "error":
            messagebox.showerror(titulo, mensagem)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensagem)