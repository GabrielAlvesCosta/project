from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
# VEM DOS MODELS
from models.repositorio import RepositorioUsuarios
from utils.validacoes import sanitizar_cpf
# BLUEPRINT agrupa rotas
auth_bp = Blueprint('auth', __name__, template_folder='../views/templates')

repo = RepositorioUsuarios()
# PAGINA INICIAL 
@auth_bp.route("/")
def home():
    return render_template("login.html")
# LOGIN
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email        = request.form.get("email", "")
        senha        = request.form.get("senha", "")

        usuario = repo.buscar_por_cpf(email)

        if usuario and check_password_hash(usuario.senha, senha):
            session["id"] = usuario.id
            session['email'] = usuario.email
            flash(f"Bem-vindo, {usuario.email}!", "sucesso")
            return redirect(url_for("usuario.listar_usuarios"))
        
        flash("Email ou Senha inválidos!", "erro")
    
    return render_template("login.html")
# LOGOUT
@auth_bp.route("/logout")
def logout():
    session.clear() 
    flash("Você saiu da sua conta com sucesso.", "sucesso")
    return redirect(url_for("auth.login"))