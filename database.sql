create database database1;

use database1;

CREATE TABLE usuarios (
   id INT AUTO_INCREMENT PRIMARY KEY,
   email VARCHAR(100) UNIQUE,
   senha VARCHAR(255),
   ativo BOOLEAN DEFAULT TRUE,
   tentativas_login INT DEFAULT 0,
   ultimo_login DATETIME
);

insert into usuarios (email, senha, ativo)
values ('usuario@teste.com', senha, TRUE);

select * from usuarios;

ALTER TABLE usuarios ADD COLUMN bloqueado_ate DATETIME NULL;