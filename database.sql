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

select * from usuarios;

UPDATE usuarios SET senha = 'scrypt:32768:8:1$gm7CLEYhLxpfMfcP$09ff4fd9507b5afccab3e45ad73dd08d3a72ea0853358f1cd4a14586f324c768bf4de51c2ca511b64b237422aa3adb4a6ceee81b9087f9f393129d033fa31df7'
 WHERE senha = '0' OR senha IS NULL;
 
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
 