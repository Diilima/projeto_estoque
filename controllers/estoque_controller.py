from models.estoque_model import EstoqueModel
from views.estoque_view import EstoqueView

class EstoqueController:
    """Controller para gerenciar lógica de negócio"""
    
    def __init__(self, view: EstoqueView):
        self.view = view
        self.usuario_atual = "admin"
        
        # Conecta callbacks da view
        self.view.on_adicionar_produto = self.adicionar_produto
        self.view.on_entrada_insumo = self.registrar_entrada
        self.view.on_saida_insumo = self.registrar_saida
        self.view.on_gerar_relatorio = self.gerar_relatorio
        self.view.on_listar_produtos = self.listar_produtos
        self.view.on_atualizar_alertas = self.atualizar_alertas
        
        # Carrega dados iniciais
        self.listar_produtos()
        self.atualizar_alertas()
    
    def adicionar_produto(self, dados: dict):
        """Adiciona novo produto"""
        try:
            nome = dados['nome'].strip()
            if not nome:
                raise ValueError("Nome do produto é obrigatório")
            
            qtd_minima = int(dados['qtd_minima'])
            preco = float(dados['preco'].replace(',', '.'))
            
            id_novo = EstoqueModel.adicionar_produto(
                nome=nome,
                descricao=dados['descricao'].strip(),
                qtd_minima=qtd_minima,
                preco=preco
            )
            
            self.view.mostrar_mensagem("Sucesso", 
                f"Produto cadastrado com ID: {id_novo}", "info")
            self.listar_produtos()
            
        except ValueError as e:
            self.view.mostrar_mensagem("Erro de Validação", str(e), "error")
        except Exception as e:
            self.view.mostrar_mensagem("Erro", f"Erro ao adicionar produto: {e}", "error")
    
    def registrar_entrada(self, dados: dict):
        """Registra entrada de insumos"""
        try:
            id_produto = int(dados['id_produto'])
            quantidade = int(dados['quantidade'])
            
            if quantidade <= 0:
                raise ValueError("Quantidade deve ser maior que zero")
            
            EstoqueModel.registrar_entrada(
                id_produto=id_produto,
                quantidade=quantidade,
                observacao=dados['observacao'],
                usuario=self.usuario_atual
            )
            
            self.view.mostrar_mensagem("Sucesso", 
                f"Entrada de {quantidade} unidades registrada!", "info")
            self.listar_produtos()
            self.atualizar_alertas()
            
        except ValueError as e:
            self.view.mostrar_mensagem("Erro de Validação", str(e), "error")
        except Exception as e:
            self.view.mostrar_mensagem("Erro", f"Erro ao registrar entrada: {e}", "error")
    
    def registrar_saida(self, dados: dict):
        """Registra saída de insumos"""
        try:
            id_produto = int(dados['id_produto'])
            quantidade = int(dados['quantidade'])
            
            if quantidade <= 0:
                raise ValueError("Quantidade deve ser maior que zero")
            
            EstoqueModel.registrar_saida(
                id_produto=id_produto,
                quantidade=quantidade,
                observacao=dados['observacao'],
                usuario=self.usuario_atual
            )
            
            self.view.mostrar_mensagem("Sucesso", 
                f"Saída de {quantidade} unidades registrada!", "info")
            self.listar_produtos()
            self.atualizar_alertas()
            
        except ValueError as e:
            self.view.mostrar_mensagem("Erro de Validação", str(e), "error")
        except Exception as e:
            self.view.mostrar_mensagem("Erro", f"Erro ao registrar saída: {e}", "error")
    
    def listar_produtos(self):
        """Atualiza lista de produtos na interface"""
        try:
            produtos = EstoqueModel.listar_produtos()
            self.view.atualizar_lista_produtos(produtos)
        except Exception as e:
            self.view.mostrar_mensagem("Erro", f"Erro ao listar produtos: {e}", "error")
    
    def atualizar_alertas(self):
        """Atualiza alertas de estoque crítico"""
        try:
            produtos_criticos = EstoqueModel.produtos_criticos()
            self.view.atualizar_alertas(produtos_criticos)
        except Exception as e:
            self.view.mostrar_mensagem("Erro", f"Erro ao carregar alertas: {e}", "error")
    
    def gerar_relatorio(self, filtros: dict):
        """Gera relatório de movimentações"""
        try:
            data_inicio = filtros['data_inicio'] if filtros['data_inicio'] != "AAAA-MM-DD" else None
            data_fim = filtros['data_fim'] if filtros['data_fim'] != "AAAA-MM-DD" else None
            
            movimentacoes = EstoqueModel.relatorio_movimentacoes(data_inicio, data_fim)
            
            # Formata relatório
            relatorio = "=" * 100 + "\n"
            relatorio += " " * 30 + "RELATÓRIO DE MOVIMENTAÇÕES DE ESTOQUE\n"
            relatorio += "=" * 100 + "\n\n"
            
            if data_inicio or data_fim:
                relatorio += f"Período: {data_inicio or 'Início'} até {data_fim or 'Hoje'}\n\n"
            
            total_entradas = 0
            total_saidas = 0
            
            relatorio += f"{'ID':<6} {'Data/Hora':<20} {'Tipo':<10} {'Produto':<35} {'Qtd':<8} {'Usuário':<12}\n"
            relatorio += "-" * 100 + "\n"
            
            for mov in movimentacoes:
                data_formatada = mov['data_movimentacao'].strftime("%d/%m/%Y %H:%M:%S")
                relatorio += f"{mov['id_movimentacao']:<6} "
                relatorio += f"{data_formatada:<20} "
                relatorio += f"{mov['tipo_movimentacao']:<10} "
                relatorio += f"{mov['nome_produto'][:35]:<35} "
                relatorio += f"{mov['quantidade']:<8} "
                relatorio += f"{mov['usuario']:<12}\n"
                
                if mov['tipo_movimentacao'] == 'ENTRADA':
                    total_entradas += mov['quantidade']
                else:
                    total_saidas += mov['quantidade']
            
            relatorio += "\n" + "=" * 100 + "\n"
            relatorio += f"TOTAL DE ENTRADAS: {total_entradas}\n"
            relatorio += f"TOTAL DE SAÍDAS: {total_saidas}\n"
            relatorio += f"SALDO LÍQUIDO: {total_entradas - total_saidas}\n"
            relatorio += "=" * 100
            
            self.view.exibir_relatorio(relatorio)
            
        except Exception as e:
            self.view.mostrar_mensagem("Erro", f"Erro ao gerar relatório: {e}", "error")