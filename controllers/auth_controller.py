from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
# VEM DOS MODELS
from models.repositorio import RepositorioUsuarios
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
        hora_atual = datetime.now().hour
        if not (8 <= hora_atual < 18):
            flash("O acesso ao sistema só é permitido entre 08h e 18h.", "erro")
            return render_template("login.html")
        email        = request.form.get("email", "")
        senha        = request.form.get("senha", "")

        usuario = repo.buscar_por_cpf(email)

        if usuario:
            if usuario.bloqueado_ate and datetime.now() < usuario.bloqueado_ate:
                tempo_restante = int((usuario.bloqueado_ate - datetime.now()).total_seconds() / 60)
                flash(f"Conta bloqueada. Tente novamente em {tempo_restante} minutos.", "erro")
                return render_template("login.html")

        if check_password_hash(usuario.senha, senha):
                usuario.tentativas_login = 0
                usuario.bloqueado_ate = None
                
            if usuario.ultimo_login is None:
                    session["id"] = usuario.id
                    session['email'] = usuario.email
                    repo.atualizar(usuario)
                    flash("Este é o seu primeiro acesso. Por favor, troque sua senha.", "sucesso")                    # Redireciona para a rota da página de primeiro acesso
                    return redirect(url_for("auth.primeiro_acesso"))
            
        usuario.ultimo_login = datetime.now()
        repo.atualizar(usuario)

        if usuario and check_password_hash(usuario.senha, senha):
            session["id"] = usuario.id
            session['email'] = usuario.email
            flash(f"Bem-vindo, {usuario.email}!", "sucesso")
            return redirect(url_for("usuario.listar_usuarios"))
        
        else:
            usuario.tentativas_login += 1
            if usuario.tentativas_login >= 3:
                    usuario.bloqueado_ate = datetime.now() + timedelta(minutes=30)
                    flash("Você errou a senha 3 vezes. Conta bloqueada por 30 minutos.", "erro")
                else:
                    tentativas_restantes = 3 - usuario.tentativas_login
                    flash(f"Email ou Senha inválidos! Você tem mais {tentativas_restantes} tentativa(s).", "erro")
                
                repo.atualizar(usuario)

        flash("Email ou Senha inválidos!", "erro")
    
    return render_template("login.html")
# LOGOUT
@auth_bp.route("/logout")
def logout():
    session.clear() 
    flash("Você saiu da sua conta com sucesso.", "sucesso")
    return redirect(url_for("auth.login"))