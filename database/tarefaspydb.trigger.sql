-- Banco de dados "tarefaspydb" --

DROP DATABASE IF EXISTS tarefaspydb;

CREATE DATABASE tarefaspydb 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_general_ci;

USE tarefaspydb;

CREATE TABLE task(
    id INT PRIMARY KEY AUTO_INCREMENT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(127) NOT NULL,
    description TEXT NOT NULL,
    expire DATETIME DEFAULT NULL,
    status ENUM('pen', 'com', 'del') DEFAULT 'pen'
    -- pen = pending(pendente) || com = completed(concluída) || del = deleted(apagada)
    /*priority ENUM('low', 'medium', 'high') DEFAULT 'medium';*/
);

DROP TRIGGER IF EXISTS before_insert_task;

DELIMITER //

CREATE TRIGGER before_insert_task
BEFORE INSERT ON task
FOR EACH ROW
BEGIN
    IF NEW.expire IS NULL THEN
        SET NEW.expire = DATE_ADD(NOW(), INTERVAL 30 DAY);
    END IF;
END;

//

DELIMITER ;
