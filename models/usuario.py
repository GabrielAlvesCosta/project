from datetime import datetime

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
        usuario.id      = dados.get("id", str(uuid.uuid4()))
        usuario.email   = dados.get("email", " ")
        usuario.senha   = dados.get("senha", "")
        usuario.ativo = dados.get("ativo", " ")
        usuario.tentativas_login = dados.get("tentativas_login,", " ")
        usuario.ultimo_login = dados.get("ultimo_login", " ")
        usuario.bloqueado_ate = dados.get("bloqueado_ate"," ")
        return usuario
    
    def _repr_(self) -> str:
        return f"<Usuario email={self.email}"