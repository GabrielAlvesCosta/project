import mysql.connector
from datetime import datetime
from mysql.connector import Error

class Usuario:
    
    def __init__(self, email: str, senha: str, id: int | None = None, ativo: bool = True, tentativas_login: int = 0, 
                 ultimo_login: datetime | None = None,bloqueado_ate: datetime | None = None):
        self.id = id
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.tentativas_login = tentativas_login
        self.ultimo_login = ultimo_login
        self.bloqueado_ate = bloqueado_ate

    def to_dict(self):
        return {
                "id" : self.id,
                "email" : self.email,
                "senha" : self.senha,
                "ativo" : self.ativo,
                "tentativas_login" : self.tentativas_login,
                "ultimo_login" : self.ultimo_login,
                "bloqueado_ate" : self.bloqueado_ate
            }
    
    @classmethod
    def from_dict(cls, dados:dict) -> "Usuario":
        usuario         = cls.__new__(cls)
        usuario.id      = dados.get("id")
        usuario.email   = dados.get("email")
        usuario.senha   = dados.get("senha")
        usuario.ativo = dados.get("ativo", True)
        tentativas = dados.get("tentativas_login")
        usuario.tentativas_login = int(tentativas) if tentativas else 0
        usuario.ultimo_login = dados.get("ultimo_login")
        usuario.bloqueado_ate = dados.get("bloqueado_ate")
        return usuario
    
    def _repr_(self) -> str:
        return f"<Usuario email={self.email}"

    def __init__(self):
        self.connection_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'database1'
        }
    
    def _get_connection(self):
        try:
            connection = mysql.connector.connect(**self.connection_config)
            return connection
        except Error as e:
            print(f"Erro ao conectar ao Mysql: {e}")
            return None

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
        
    def buscar_por_email(self, email: str) -> Usuario | None:
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
            ultimo_login,
            bloqueado_ate)
            VALUES(%s, %s, %s, %s, %s, %s)"""
            if str(usuario.tentativas_login).strip() == "" or usuario.tentativas_login is None:
                usuario.tentativas_login = 0
            if usuario.ultimo_login in ("[]", "", " ", None):
                usuario.ultimo_login = None
            if usuario.bloqueado_ate in ("[]", "", " ", None):
                usuario.bloqueado_ate = None
            valores = (usuario.email, usuario.senha, usuario.ativo, 
                       usuario.tentativas_login, usuario.ultimo_login, usuario.bloqueado_ate)
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
            sql = """UPDATE usuarios SET senha=%s, tentativas_login=%s, ultimo_login=%s, bloqueado_ate=%s WHERE email=%s"""
            valores = (
                        usuario_atualizado.senha,usuario_atualizado.tentativas_login, usuario_atualizado.ultimo_login,
                        usuario_atualizado.bloqueado_ate, usuario_atualizado.email
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