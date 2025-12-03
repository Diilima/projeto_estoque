-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS sistema_estoque;
USE sistema_estoque;

-- Tabela de produtos
CREATE TABLE IF NOT EXISTS produtos (
    id_produto INT AUTO_INCREMENT PRIMARY KEY,
    nome_produto VARCHAR(100) NOT NULL,
    descricao TEXT,
    qtd_estoque INT DEFAULT 0,
    qtd_minima INT DEFAULT 10,
    preco_unitario DECIMAL(10,2),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de movimentações
CREATE TABLE IF NOT EXISTS movimentacoes (
    id_movimentacao INT AUTO_INCREMENT PRIMARY KEY,
    id_produto INT,
    tipo_movimentacao ENUM('ENTRADA', 'SAIDA') NOT NULL,
    quantidade INT NOT NULL,
    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observacao TEXT,
    usuario VARCHAR(50),
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);

-- Índices para performance
CREATE INDEX idx_produto_mov ON movimentacoes(id_produto);
CREATE INDEX idx_tipo_mov ON movimentacoes(tipo_movimentacao);
CREATE INDEX idx_data_mov ON movimentacoes(data_movimentacao);

-- Inserir dados de exemplo
INSERT INTO produtos (nome_produto, descricao, qtd_estoque, qtd_minima, preco_unitario) VALUES
('Parafuso M6', 'Parafuso métrico 6mm', 50, 100, 0.25),
('Arruela Lisa', 'Arruela lisa galvanizada', 30, 200, 0.10),
('Porca M6', 'Porca sextavada M6', 45, 150, 0.15);

