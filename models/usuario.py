import uuid# usado para gerar IDs únicos (uuid4
#def são METODOS
class Usuario:
    
    def __init__(self, nome: str , cpf_limpo: str, email: str, idade: int, senha: str):
        self.id = str(uuid.uuid4())
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.tentativas_login = tentativas_login
        self.ultimo_login = ultimo_login

    def eh_maior_de_idade(self):
        return self.idade >= 18
        
    def to_dict(self):
        return {
                "id" : self.id,
                "email" : self.email,
                "senha" : self.senha,
                "ativo" : self.ativo,
                "tentativas_login" : self.tentativas_login,
                "ultimo_login" : self.ultimo_login
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
        return usuario
    
    def _repr_(self) -> str:
        return f"<Usuario email={self.email}"