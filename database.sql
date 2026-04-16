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

ALTER TABLE usuarios ADD COLUMN bloqueado_ate DATETIME NULL;

insert into usuarios (email, senha, ativo)
values ('usuario@teste.com', senha, TRUE);

insert into usuarios (email, senha, ativo)
values ('teste@teste.com', NULL, TRUE);

insert into usuarios (email, senha, ativo)
values ('analise@teste.com', 0, TRUE);

select * from usuarios;
 
 UPDATE usuarios SET bloqueado_ate = NUll
 WHERE tentativas_login = '3' OR tentativas_login = '4';

UPDATE usuarios SET tentativas_login = 0
WHERE tentativas_login = '3' OR tentativas_login = '4';
 
UPDATE usuarios SET ultimo_login = NULL
WHERE id = '1' or id = '2' or id = '3' or id = '4' or id = '8';

UPDATE usuarios SET senha = NULL
WHERE id = '17' or id = '23' or id = '29' or id = '30';

DELETE FROM usuarios 
WHERE id = 8;
 
