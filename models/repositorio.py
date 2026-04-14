import mysql.connector

from mysql.connector import Error
from models.usuario import Usuario
from utils.validacoes import sanitizar_cpf

class RepositorioUsuarios:
#-------Banco de Dados----------------
    def __init__(self):
        self.connection_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'admin',
            'database': 'database1'
        }
    
    def _get_connection(self):
        try:
            connection = mysql.connector.connect(**self.connection_config)
            return connection
        except Error as e:
            print(f"Erro ao conectar ao Mysql: {e}")
            return None

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
        
    def buscar_por_cpf(self, email: str) -> Usuario | None:
        connection = self._get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            row = cursor.fetchone()
            return Usuario.from_dict(row) if row else None
        except Error as e:
            print(f"Erro ao buscar usuario pelo Email: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
#------Escritra-------------
    def salvar(self, usuario: Usuario) -> bool:
        connection = self._get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            sql = """INSERT INTO usuarios (
            email, 
            senha,
            ativo,
            tentativas_login,
            ultimo_login)
            VALUES(%s, %s, %s, %s, %s)"""
            if str(usuario.tentativas_login).strip() == "" or usuario.tentativas_login is None:
                usuario.tentativas_login = 0
            if usuario.ultimo_login in ("[]", "", " ", None):
                usuario.ultimo_login = None
            valores = (usuario.email, usuario.senha, usuario.ativo, 
                       usuario.tentativas_login, usuario.ultimo_login)
            cursor.execute(sql, valores)
            connection.commit()
            return True
        except Error as e:
            print(f"Erro ao ssalvar o usuário: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def atualizar(self, usuario_atualizado: Usuario) -> bool:
        connection = self._get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            sql = """UPDATE usuarios SET senha=%s WHERE email=%s"""
            valores = (
                        usuario_atualizado.senha, usuario_atualizado.email
                    )
            cursor.execute(sql, valores)
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Erro ao atualizar o usuário: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def deletar(self, email: str) -> bool:
        connection = self._get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM usuarios WHERE email=%s")
            cursor.execute(sql, (email,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Erro ao deletar o usuário: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()