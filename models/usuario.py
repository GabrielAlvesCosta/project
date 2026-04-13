import uuid# usado para gerar IDs únicos (uuid4
#def são METODOS
class Usuario:
    
    def __init__(self, nome: str , cpf_limpo: str, email: str, idade: int, senha: str):
        self.id = str(uuid.uuid4())
        self.email = email
        self.idade = idade
        self.senha = senha

    def eh_maior_de_idade(self):
        return self.idade >= 18
        
    def to_dict(self):
        return {
                "id" : self.id,
                "nome" : self.nome,
                "cpf" : self.cpf,
                "email" : self.email,
                "idade" : self.idade,
                "senha" : self.senha,
            }
    
    @classmethod
    def from_dict(cls, dados:dict) -> "Usuario":
        usuario         = cls.__new__(cls)
        usuario.id      = dados.get("id", str(uuid.uuid4()))
        usuario.cpf     = dados.get("cpf", " ")
        usuario.nome    = dados.get("nome", "")
        usuario.email   = dados.get("email", " ")
        usuario.idade   = int(dados.get("idade", 0))
        usuario.senha   = dados.get("senha", "")
        return usuario
    
    def _repr_(self) -> str:
        return f"<Usuario nome={self.nome} cpf={self.cpf}"