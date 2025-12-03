import tkinter as tk
from views.estoque_view import EstoqueView
from controllers.estoque_controller import EstoqueController
from config.database import DatabaseConfig

def main():
    """Ponto de entrada da aplicação"""
    
    print("=" * 60)
    print(" SISTEMA DE CONTROLE DE ESTOQUE")
    print("=" * 60)
    
    # Testa conexão com BD
    print("\n🔍 Testando conexão com banco de dados...")
    if not DatabaseConfig.test_connection():
        print("\nERRO: Não foi possível conectar ao banco de dados!")
        print("Verifique:")
        print("  1. MySQL está rodando")
        print("  2. Credenciais em config/database.py")
        print("  3. Banco 'sistema_estoque' foi criado")
        input("\nPressione ENTER para sair...")
        return
    
    print("\nSistema iniciado com sucesso!")
    print("=" * 60)
    
    # Inicializa aplicação
    root = tk.Tk()
    view = EstoqueView(root)
    controller = EstoqueController(view)
    
    root.mainloop()

if __name__ == "__main__":
    main()