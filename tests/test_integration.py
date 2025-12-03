import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.estoque_model import EstoqueModel
from config.database import DatabaseConfig

class TestIntegration(unittest.TestCase):
    """Testes de integração - fluxo completo do sistema"""
    
    def test_fluxo_completo_produto(self):
        """Testa fluxo completo: cadastro → entrada → saída → relatório"""
        print("\n🔄 Testando fluxo completo do sistema...")
        
        # 1. Cadastrar produto
        print("   📦 1. Cadastrando produto...")
        id_produto = EstoqueModel.adicionar_produto(
            nome="Produto Integração",
            descricao="Teste de integração completa",
            qtd_minima=20,
            preco=25.90
        )
        self.assertIsInstance(id_produto, int)
        print(f"      ✅ Produto criado - ID: {id_produto}")
        
        # 2. Registrar entrada
        print("   📥 2. Registrando entrada de estoque...")
        sucesso_entrada = EstoqueModel.registrar_entrada(
            id_produto=id_produto,
            quantidade=100,
            observacao="Compra inicial",
            usuario="admin"
        )
        self.assertTrue(sucesso_entrada)
        print("      ✅ Entrada registrada - 100 unidades")
        
        # 3. Verificar estoque
        print("   📊 3. Verificando estoque atualizado...")
        produtos = EstoqueModel.listar_produtos()
        produto_criado = next((p for p in produtos if p['id_produto'] == id_produto), None)
        self.assertIsNotNone(produto_criado)
        self.assertEqual(produto_criado['qtd_estoque'], 100)
        print(f"      ✅ Estoque confirmado: {produto_criado['qtd_estoque']} unidades")
        
        # 4. Registrar saída
        print("   📤 4. Registrando saída de estoque...")
        sucesso_saida = EstoqueModel.registrar_saida(
            id_produto=id_produto,
            quantidade=30,
            observacao="Venda",
            usuario="admin"
        )
        self.assertTrue(sucesso_saida)
        print("      ✅ Saída registrada - 30 unidades")
        
        # 5. Verificar estoque final
        print("   📊 5. Verificando estoque final...")
        produtos = EstoqueModel.listar_produtos()
        produto_atualizado = next((p for p in produtos if p['id_produto'] == id_produto), None)
        self.assertEqual(produto_atualizado['qtd_estoque'], 70)
        print(f"      ✅ Estoque final: {produto_atualizado['qtd_estoque']} unidades")
        
        # 6. Gerar relatório
        print("   📄 6. Gerando relatório de movimentações...")
        relatorio = EstoqueModel.relatorio_movimentacoes()
        movimentacoes_produto = [m for m in relatorio if m['id_produto'] == id_produto]
        self.assertGreaterEqual(len(movimentacoes_produto), 2)
        print(f"      ✅ Relatório gerado - {len(movimentacoes_produto)} movimentações")
        
        print("\n✅ TESTE DE INTEGRAÇÃO COMPLETO - SUCESSO!")

if __name__ == '__main__':
    unittest.main(verbosity=2)