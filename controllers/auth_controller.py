from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from models.usuario_model import Usuario

auth_bp = Blueprint('auth', __name__, template_folder='../views/templates')

repo = Usuario()

@auth_bp.route("/")
def home():
    return render_template("login.html")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash("Acesso negado! Por favor, faça login para acessar esta página.", "erro")
            
            return redirect(url_for('auth.login')) 
        
        return f(*args, **kwargs)
    
    return decorated_function

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        hora_atual = datetime.now().hour
        if not (0 <= hora_atual < 23):
            flash("O acesso ao sistema só é permitido entre 08h e 18h.", "erro")
            return render_template("login.html")
        
        email        = request.form.get("email", "")
        senha        = request.form.get("senha", "")

        usuario = repo.buscar_por_email(email)

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
                    flash("Este é o seu primeiro acesso. Por favor, troque sua senha.", "sucesso")
                    return redirect(url_for("auth.editar_usuario", email=usuario.email))
            
                usuario.ultimo_login = datetime.now()
                repo.atualizar(usuario)

                session["id"] = usuario.id
                session['email'] = usuario.email
                flash(f"Bem-vindo, {usuario.email}!", "sucesso")
                return redirect(url_for("auth.listar_usuarios"))
        
            else:
                usuario.tentativas_login += 1

                if usuario.tentativas_login >= 3:
                    usuario.bloqueado_ate = datetime.now() + timedelta(minutes=30)
                    flash("Você errou a senha 3 vezes. Conta bloqueada por 30 minutos.", "erro")
                else:
                    tentativas_restantes = 3 - usuario.tentativas_login
                    flash(f"Email ou Senha inválidos! Você tem mais {tentativas_restantes} tentativa(s).", "erro")
                
                repo.atualizar(usuario)
        else:    
            flash("Email ou Senha inválidos!", "erro")
    
    return render_template("login.html")

@auth_bp.route("/dashboard", methods=["GET"])
@login_required
def listar_usuarios():
    
    usuarios= repo.listar()

    return render_template(
        "dashboard.html",
        usuarios = usuarios,
        )

@auth_bp.route("/usuario/editar/<email>", methods=["GET", "POST"])
@login_required
def editar_usuario(email):
    
    usuario = repo.buscar_por_email(email)

    if not usuario:
        flash("Usuário não encontrado", "erro")
        return redirect(url_for("usuario.listar_usuarios"))

    eh_proprio = session.get("email") == usuario.email
    
    if not eh_proprio:
        flash("Você só pode editar o seu próprio perfil!", "erro")
        return redirect(url_for("usuario.listar_usuarios"))
    
    if request.method == "GET":
        return render_template("primeiro_acesso.html", usuario=usuario)

    senha = request.form.get("senha", "")
    if senha:
        usuario.senha = generate_password_hash(senha)
        usuario.ultimo_login = datetime.now()

    if repo.atualizar(usuario):
        flash("Usuário atualizado com sucesso!", "sucesso")
    else:
        flash("Erro ao autualizar o usuário!", "erro")
 
    return redirect(url_for("auth.listar_usuarios"))

@auth_bp.route("/logout")
def logout():
    session.clear() 
    flash("Você saiu da sua conta com sucesso.", "sucesso")
    return redirect(url_for("auth.login"))

@auth_bp.after_app_request
def evitar_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response