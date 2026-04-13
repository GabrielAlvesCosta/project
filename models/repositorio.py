import mysql.connector

from mysql.connector import Error
from models.usuario import Usuario
from utils.validacoes import sanitizar_cpf

class RepositorioUsuarios:
#-------Banco de Dados----------------
    def __init__(self):
        self.connection_config = {
            'host': 'localhost',
            'user': 'mickey',
            'password': 'admin',
            'database': 'database1'
        }
    
    def _get_connection(self):
        try:
            connection = mysql.connector.connect(**self.connection_config)
            return connection
        except Error as e:
            print(f"Erro ao conectar ao Mysql: {e}")

#-----Leitura-------------
    def listar(self) -> list[Usuario]:
        connection = self._get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios")
            rows = cursor.fetchall()
            return [Usuario.from_dict(row) for row in rows]
        except Error as e:
            print(f"Erro ao listar usuários: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        
    def buscar_por_cpf(self, cpf: str) -> Usuario | None:
        connection = self._get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cpf_limpo = sanitizar_cpf(cpf)
            cursor.execute("SELECT * FROM usuarios WHERE cpf = %s", (cpf_limpo))
            row = cursor.fetchone()
            return Usuario.from_dict(row) if row else None
        except Error as e:
            print(f"Erro ao buscar usuario pelo CPF: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def cpf_existe(self, cpf: str) -> bool:
        return self.buscar_por_cpf(cpf) is not None
    
#------Escritra-------------
    def salvar(self, usuario: Usuario) -> bool:
        connection = self._get_connection()
        if not connection:
            return False
        
        try:
            cusor = connection.cursor()
            sql = """INSERT INTO usuarios (
            id,
            email, 
            senha,
            ativo,
            tentativas_login,
            ultimo_login)
            VALUeS(%s, %s, %s, %s, %s, %s)"""
            valores = (usuario.id, usuario.email, usuario.senha,
                       usuario.ativo, usuario.tentativas_login, usuario. ultimo_login)
            cusor.execute(sql, valores)
            connection.commit()
            return True
        except Error as e:
            print(f"Erro ao ssalvar o usuário: {e}")
            return False
        finally:
            if connection.is_connected():
                cusor.close()
                connection.close()

    def atualizar(self, usuario_atualizado: Usuario) -> bool:
        connection = self._get_connection()
        if not connection:
            return False
        
        try:
            cusor = connection.cursor()
            sql = """UPDATE usuarios SET nome=%s, cpf=%s, email=%s, idade=%s, senha=%s, perfil=%s
            WHERE cpf=%s"""
            valores = (
                        usuario_atualizado.nome,
                        usuario_atualizado.cpf,
                        usuario_atualizado.email,
                        usuario_atualizado.idade,
                        usuario_atualizado.senha,
                    )
            cusor.execute(sql, valores)
            connection.commit()
            return cursor.rawcount > 0
        except Error as e:
            print(f"Erro ao atualizar o usuário: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def deletar(self, cpf: str) -> bool:
        connection = self._get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cpf_limpo = sanitizar_cpf(cpf)
            cursor.execute("DELETE FROM ususarios WHERE cpf=%s", (cpf_limpo,))
            connection.commit()
            return cursor.rawcount > 0
        except Error as e:
            print(f"Erro ao deletar o usuário: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()