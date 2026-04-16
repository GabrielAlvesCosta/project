import json
from models.usuario_model import Usuario

def migrar_dados():
    try:
        with open('usuarios.json', 'r', encoding='utf=8') as f:
            dados_json = json.load(f)
    except FileNotFoundError:
        print("Arquivo usuarios.json não encontrado!")
        return
    
    repo =Usuario()

    for dados_usuario in dados_json:
        usuario = Usuario.from_dict(dados_usuario)
        if repo.salvar(usuario):
            print(f"Usuário {usuario.email} sucesso!")
        else:
            print(f"Erro ao migrar usuário {usuario.email}!")
        
    print("Migração concluida!")

if __name__ == "__main__":
    migrar_dados()