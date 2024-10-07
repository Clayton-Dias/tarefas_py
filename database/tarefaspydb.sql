-- Banco de dados "tarefaspydb" --

-- Remove o banco de dados "tarefaspydb" se ele já existir
DROP DATABASE IF EXISTS tarefaspydb;

-- Cria um novo banco de dados chamado "tarefaspydb" com charset e collation especificados
CREATE DATABASE tarefaspydb 
    CHARACTER SET utf8mb4  -- Define a codificação de caracteres como utf8mb4
    COLLATE utf8mb4_general_ci;  -- Define a collation como utf8mb4_general_ci

-- Seleciona o banco de dados "tarefaspydb" para uso
USE tarefaspydb;

-- Cria a tabela "task" no banco de dados "tarefaspydb"
CREATE TABLE task(
    id INT PRIMARY KEY AUTO_INCREMENT,  -- ID da tarefa como chave primária, auto-incrementada
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Data de criação da tarefa, padrão é o timestamp atual
    name VARCHAR(127) NOT NULL,  -- Nome da tarefa, não pode ser nulo, com tamanho máximo de 127 caracteres
    description TEXT NOT NULL,  -- Descrição da tarefa, não pode ser nula
    expire DATETIME DEFAULT NULL,  -- Data de expiração da tarefa, pode ser nula
    status ENUM('pen', 'com', 'del') DEFAULT 'pen'  -- Status da tarefa (pendente, concluída ou apagada), padrão é 'pen'
    -- pen = pending(pendente) || com = completed(concluída) || del = deleted(apagada)
    /*priority ENUM('low', 'medium', 'high') DEFAULT 'medium';*/  -- Comentado: prioridade da tarefa (baixo, médio, alto), padrão é 'medium'
);

