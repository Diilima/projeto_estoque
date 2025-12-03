import mysql.connector
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class DatabaseConfig:
    """Configuração centralizada do banco de dados MySQL"""
    
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', '1234'),
        'database': os.getenv('DB_NAME', 'sistema_estoque'),
        'auth_plugin': 'mysql_native_password'
    }
    
    @staticmethod
    def get_connection():
        """
        Estabelece conexão com o banco de dados
        
        Returns:
            mysql.connector.connection: Objeto de conexão
            
        Raises:
            mysql.connector.Error: Se falhar ao conectar
        """
        try:
            conn = mysql.connector.connect(**DatabaseConfig.DB_CONFIG)
            return conn
        except mysql.connector.Error as err:
            config_seguro = DatabaseConfig.DB_CONFIG.copy()
            config_seguro['password'] = '***OCULTO***'
            print(f"❌ Erro ao conectar ao banco de dados:")
            print(f"   Configuração: {config_seguro}")
            print(f"   Erro: {err}")
            raise
    
    @staticmethod
    def test_connection():
        """
        Testa conexão com banco de dados
        
        Returns:
            bool: True se conexão bem sucedida, False caso contrário
        """
        conn = None
        cursor = None
        try:
            conn = DatabaseConfig.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ Conexão bem sucedida! MySQL versão: {version[0]}")
            return True
        except mysql.connector.Error as err:
            print(f"❌ Falha no teste de conexão: {err}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def init_database():
        """
        Inicializa o banco de dados com as tabelas necessárias
        
        Returns:
            bool: True se inicialização bem sucedida
        """
        conn = None
        cursor = None
        try:
            conn = DatabaseConfig.get_connection()
            cursor = conn.cursor()
            
            # Lê e executa o script SQL
            with open('sql/database.sql', 'r', encoding='utf-8') as f:
                sql_script = f.read()
                
            # Executa cada comando SQL separadamente
            for statement in sql_script.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            
            conn.commit()
            print("✅ Banco de dados inicializado com sucesso!")
            return True
            
        except mysql.connector.Error as err:
            print(f"❌ Erro ao inicializar banco: {err}")
            if conn:
                conn.rollback()
            return False
        except FileNotFoundError:
            print("❌ Arquivo sql/database.sql não encontrado!")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()