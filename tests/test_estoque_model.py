import unittest
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.estoque_model import EstoqueModel
from config.database import DatabaseConfig

class TestEstoqueModel(unittest.TestCase):
    """Testes unitários para o EstoqueModel"""
    
    @classmethod
    def setUpClass(cls):
        """Configuração inicial antes de todos os testes"""
        print("\n🧪 Iniciando testes do EstoqueModel...")
        # Testa conexão com banco
        assert DatabaseConfig.test_connection(), "Falha na conexão com banco de dados"
    
    def test_01_conexao_banco(self):
        """Testa se consegue conectar ao banco de dados"""
        conexao = DatabaseConfig.get_connection()
        self.assertIsNotNone(conexao, "Conexão não deve ser None")
        conexao.close()
    
    def test_02_adicionar_produto(self):
        """Testa adição de produto"""
        try:
            id_produto = EstoqueModel.adicionar_produto(
                nome="Produto Teste Unitário",
                descricao="Descrição de teste",
                qtd_minima=10,
                preco=15.50
            )
            self.assertIsInstance(id_produto, int, "ID deve ser inteiro")
            self.assertGreater(id_produto, 0, "ID deve ser maior que zero")
            print(f"   ✅ Produto criado com ID: {id_produto}")
        except Exception as e:
            self.fail(f"Falha ao adicionar produto: {e}")
    
    def test_03_listar_produtos(self):
        """Testa listagem de produtos"""
        try:
            produtos = EstoqueModel.listar_produtos()
            self.assertIsInstance(produtos, list, "Deve retornar uma lista")
            if len(produtos) > 0:
                produto = produtos[0]
                self.assertIn('id_produto', produto, "Deve ter id_produto")
                self.assertIn('nome_produto', produto, "Deve ter nome_produto")
                print(f"   ✅ {len(produtos)} produtos encontrados")
        except Exception as e:
            self.fail(f"Falha ao listar produtos: {e}")
    
    def test_04_registrar_entrada(self):
        """Testa registro de entrada de estoque"""
        try:
            # Primeiro adiciona um produto
            id_produto = EstoqueModel.adicionar_produto(
                nome="Teste Entrada",
                descricao="Produto para teste de entrada",
                qtd_minima=5,
                preco=10.00
            )
            
            # Registra entrada
            sucesso = EstoqueModel.registrar_entrada(
                id_produto=id_produto,
                quantidade=50,
                observacao="Entrada de teste",
                usuario="teste_automatizado"
            )
            
            self.assertTrue(sucesso, "Entrada deve ser registrada com sucesso")
            print(f"   ✅ Entrada registrada para produto ID: {id_produto}")
        except Exception as e:
            self.fail(f"Falha ao registrar entrada: {e}")
    
    def test_05_registrar_saida(self):
        """Testa registro de saída de estoque"""
        try:
            # Adiciona produto e faz entrada
            id_produto = EstoqueModel.adicionar_produto(
                nome="Teste Saída",
                descricao="Produto para teste de saída",
                qtd_minima=5,
                preco=10.00
            )
            
            EstoqueModel.registrar_entrada(
                id_produto=id_produto,
                quantidade=100,
                observacao="Entrada inicial",
                usuario="teste_automatizado"
            )
            
            # Registra saída
            sucesso = EstoqueModel.registrar_saida(
                id_produto=id_produto,
                quantidade=30,
                observacao="Saída de teste",
                usuario="teste_automatizado"
            )
            
            self.assertTrue(sucesso, "Saída deve ser registrada com sucesso")
            print(f"   ✅ Saída registrada para produto ID: {id_produto}")
        except Exception as e:
            self.fail(f"Falha ao registrar saída: {e}")
    
    def test_06_estoque_insuficiente(self):
        """Testa se impede saída com estoque insuficiente"""
        try:
            # Adiciona produto com estoque baixo
            id_produto = EstoqueModel.adicionar_produto(
                nome="Teste Estoque Insuficiente",
                descricao="Produto para teste de validação",
                qtd_minima=5,
                preco=10.00
            )
            
            EstoqueModel.registrar_entrada(
                id_produto=id_produto,
                quantidade=10,
                observacao="Entrada mínima",
                usuario="teste_automatizado"
            )
            
            # Tenta saída maior que estoque
            with self.assertRaises(Exception) as context:
                EstoqueModel.registrar_saida(
                    id_produto=id_produto,
                    quantidade=50,
                    observacao="Tentativa de saída excessiva",
                    usuario="teste_automatizado"
                )
            
            self.assertIn("insuficiente", str(context.exception).lower())
            print(f"   ✅ Validação de estoque funcionando corretamente")
            
        except AssertionError:
            raise
        except Exception as e:
            self.fail(f"Falha inesperada: {e}")
    
    def test_07_produtos_criticos(self):
        """Testa identificação de produtos com estoque crítico"""
        try:
            produtos_criticos = EstoqueModel.produtos_criticos()
            self.assertIsInstance(produtos_criticos, list, "Deve retornar lista")
            print(f"   ✅ {len(produtos_criticos)} produtos críticos identificados")
        except Exception as e:
            self.fail(f"Falha ao buscar produtos críticos: {e}")
    
    def test_08_relatorio_movimentacoes(self):
        """Testa geração de relatório de movimentações"""
        try:
            relatorio = EstoqueModel.relatorio_movimentacoes()
            self.assertIsInstance(relatorio, list, "Deve retornar lista")
            print(f"   ✅ Relatório gerado com {len(relatorio)} movimentações")
        except Exception as e:
            self.fail(f"Falha ao gerar relatório: {e}")

def run_tests():
    """Executa os testes e gera relatório"""
    print("\n" + "="*60)
    print("🧪 EXECUTANDO SUITE DE TESTES - SISTEMA DE ESTOQUE")
    print("="*60)
    
    # Cria suite de testes
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestEstoqueModel)
    
    # Executa testes com verbosidade
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    print(f"✅ Testes executados: {result.testsRun}")
    print(f"✅ Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"❌ Erros: {len(result.errors)}")
    print("="*60)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)