from config.database import DatabaseConfig
from typing import List, Dict, Optional

class EstoqueModel:
    """Modelo para operações de estoque"""
    
    @staticmethod
    def listar_produtos() -> List[Dict]:
        """Retorna todos os produtos"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT id_produto, nome_produto, descricao, 
                       qtd_estoque, qtd_minima, preco_unitario
                FROM produtos
                ORDER BY nome_produto
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def adicionar_produto(nome: str, descricao: str, qtd_minima: int, preco: float) -> int:
        """Adiciona novo produto"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO produtos (nome_produto, descricao, qtd_minima, preco_unitario)
                VALUES (%s, %s, %s, %s)
            """, (nome, descricao, qtd_minima, preco))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def registrar_entrada(id_produto: int, quantidade: int, observacao: str, usuario: str) -> bool:
        """Registra entrada de insumos"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        try:
            # Registra movimentação
            cursor.execute("""
                INSERT INTO movimentacoes 
                (id_produto, tipo_movimentacao, quantidade, observacao, usuario)
                VALUES (%s, 'ENTRADA', %s, %s, %s)
            """, (id_produto, quantidade, observacao, usuario))
            
            # Atualiza estoque
            cursor.execute("""
                UPDATE produtos 
                SET qtd_estoque = qtd_estoque + %s 
                WHERE id_produto = %s
            """, (quantidade, id_produto))
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def registrar_saida(id_produto: int, quantidade: int, observacao: str, usuario: str) -> bool:
        """Registra saída de insumos"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        try:
            # Verifica disponibilidade
            cursor.execute("SELECT qtd_estoque FROM produtos WHERE id_produto = %s", (id_produto,))
            resultado = cursor.fetchone()
            
            if not resultado:
                raise Exception(f"Produto ID {id_produto} não encontrado")
            
            estoque_atual = resultado[0]
            
            if estoque_atual < quantidade:
                raise Exception(f"Estoque insuficiente. Disponível: {estoque_atual}")
            
            # Registra movimentação
            cursor.execute("""
                INSERT INTO movimentacoes 
                (id_produto, tipo_movimentacao, quantidade, observacao, usuario)
                VALUES (%s, 'SAIDA', %s, %s, %s)
            """, (id_produto, quantidade, observacao, usuario))
            
            # Atualiza estoque
            cursor.execute("""
                UPDATE produtos 
                SET qtd_estoque = qtd_estoque - %s 
                WHERE id_produto = %s
            """, (quantidade, id_produto))
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def produtos_criticos() -> List[Dict]:
        """Retorna produtos abaixo do estoque mínimo"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT id_produto, nome_produto, qtd_estoque, qtd_minima,
                       (qtd_minima - qtd_estoque) as deficit
                FROM produtos
                WHERE qtd_estoque < qtd_minima
                ORDER BY deficit DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def relatorio_movimentacoes(data_inicio: str = None, data_fim: str = None) -> List[Dict]:
        """Gera relatório de movimentações"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            query = """
                SELECT m.id_movimentacao, p.nome_produto, m.tipo_movimentacao,
                       m.quantidade, m.data_movimentacao, m.observacao, m.usuario
                FROM movimentacoes m
                JOIN produtos p ON m.id_produto = p.id_produto
                WHERE 1=1
            """
            params = []
            
            if data_inicio and data_inicio != "AAAA-MM-DD":
                query += " AND DATE(m.data_movimentacao) >= %s"
                params.append(data_inicio)
            
            if data_fim and data_fim != "AAAA-MM-DD":
                query += " AND DATE(m.data_movimentacao) <= %s"
                params.append(data_fim)
            
            query += " ORDER BY m.data_movimentacao DESC LIMIT 100"
            
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()