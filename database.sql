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

UPDATE usuarios SET senha = 'scrypt:32768:8:1$gm7CLEYhLxpfMfcP$09ff4fd9507b5afccab3e45ad73dd08d3a72ea0853358f1cd4a14586f324c768bf4de51c2ca511b64b237422aa3adb4a6ceee81b9087f9f393129d033fa31df7'
 WHERE senha = '0' OR senha IS NULL;
 
 UPDATE usuarios SET bloqueado_ate = NUll
 WHERE tentativas_login = '3' OR tentativas_login = '4';

UPDATE usuarios SET tentativas_login = 0
WHERE tentativas_login = '3' OR tentativas_login = '4';
 
UPDATE usuarios SET senha = NULL
WHERE email = 'gollumalvescosta@gmail.com';

UPDATE usuarios SET ultimo_login = NULL
WHERE email = 'usuario@teste.com';


 