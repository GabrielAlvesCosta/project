from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash 
from werkzeug.security import generate_password_hash

from models.repositorio import RepositorioUsuarios

usuario_bp = Blueprint('usuario', __name__, template_folder='../views/templates')

repo = RepositorioUsuarios()

def _usuario_logado() -> bool:
    return "id" in session

# LISTAGEM
@usuario_bp.route("/dashboard", methods=["GET"])
def listar_usuarios():
    if not _usuario_logado():
        flash("Você precisa estar logado!", "erro")
        return redirect(url_for("auth.login"))
    
    usuarios= repo.listar()

    return render_template(
        "dashboard.html",
        usuarios = usuarios, #FUNÇÂO = VARIAVEL
        )

# EDIÇÂO
@usuario_bp.route("/usuario/editar/<email>", methods=["GET", "POST"])
def editar_usuario(email):
    if not _usuario_logado():
        flash("Não autorizado!", "erro")
        return redirect(url_for("auth.login"))
    
    usuario = repo.buscar_por_cpf(email)

    if not usuario:
        flash("Usuário não encontrado", "erro")
        return redirect(url_for("usuario.listar_usuarios"))
    # PERMIÇÔES: ADMIN=TODOS COMUM=SELF
    _eh_admin = session.get("cargo") == "admin"

    eh_proprio = session.get("email") == usuario.email
    
    if not _eh_admin and not eh_proprio:
        flash("Você só pode editar o seu próprio perfil!", "erro")
        return redirect(url_for("usuario.listar_usuarios"))
    
    if request.method == "GET":
        return render_template("primeiro_acesso.html", usuario=usuario)

    senha = request.form.get("senha", "")
    if senha:
        usuario.senha = generate_password_hash(senha)

    if repo.atualizar(usuario):
        flash("Usuário atualizado com sucesso!", "sucesso")
    else:
        flash("Erro ao autualizar o usuário!", "erro")
 
    return redirect(url_for("usuario.listar_usuarios"))