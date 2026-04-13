create database database1;

CREATE TABLE usuarios (
   id INT AUTO_INCREMENT PRIMARY KEY,
   email VARCHAR(100) UNIQUE,
   senha VARCHAR(255),
   ativo BOOLEAN DEFAULT TRUE,
   tentativas_login INT DEFAULT 0,
   ultimo_login DATETIME
);