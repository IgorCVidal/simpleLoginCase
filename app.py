from flask import Flask, flash, request, url_for, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from dataclasses import dataclass
import smtplib


app = Flask(__name__)
app.config['SECRET_KEY'] = 'segundavez'

# Construtor de usuarios


@dataclass
class Users:
    login: str
    senha: str
    cpf: str

    def authcpf(cpf):
        for i in lista_usuarios:
            if i.cpf == cpf:
                return i
# Função para envio de email.


def enviar_email(email, body):
    sender = 'NossoEmail@email.com'
    receivers = [email]

    message = f"""
    From: NossoEmail@email.com
    To: {email}
    Seus dados para login: {body}"""

    smtpObj = smtplib.SMTP('localhost', 1025, 'localhost')
    smtpObj.sendmail(sender, receivers, message)


# Registrando usuarios para test
admin = Users('admin', 'admin', '1234')
user1 = Users('user', 'user', '4321')

lista_usuarios = []
lista_usuarios.append(admin)
lista_usuarios.append(user1)

# Formularios e seus requerimentos


class RecoverForm(FlaskForm):

    usercpf = StringField(validators=[InputRequired(), Length(
        min=3, max=10)], render_kw={"placeholder": "CPF"})
    useremail = StringField(validators=[InputRequired(), Length(
        min=3, max=20)], render_kw={"placeholder": "Email"})
    submit = SubmitField("Enviar")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=3, max=20)], render_kw={"placeholder": "Usuario"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=3, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Entrar")


class NovaSenhaForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=3, max=20)], render_kw={"placeholder": "Usuario"})
    novasenha = PasswordField(validators=[InputRequired(), Length(
        min=3, max=20)], render_kw={"placeholder": "Nova Senha"})
    submit = SubmitField("Entrar")

# Rotas das paginas


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = NovaSenhaForm()
    # Validação e atualização de senha
    if request.method == "POST":
        username = form.username.data
        password = form.novasenha.data
        for i in lista_usuarios:
            if i.login == username:
                i.senha = password
                flash("Senha alterada com sucesso.")

    return render_template('dashboard.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Validação do login.
    if request.method == "POST":
        username = form.username.data
        password = form.password.data

        for i in lista_usuarios:
            if i.login == username and i.senha == password:
                return redirect(url_for('dashboard'))

        else:
            flash('Usuario ou senha incorreto.')

    return render_template('login.html', form=form)


@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    form = RecoverForm()
    # Validação do CPF. Envio de email não implementado.
    if request.method == "POST":
        usercpf = form.usercpf.data
        email = form.useremail.data

        if any(x for x in lista_usuarios if x.cpf == usercpf):
            user = Users.authcpf(usercpf)

            enviar_email(email, user)
            flash(
                "MSN004 - Dados de acesso ao sistema foram enviados para o e-mail informado")
            flash(f"Login: {user.login} Senha: {user.senha}")
        else:
            flash('MSN001 - Usuário não está cadastrado no sistema!')

    return render_template('recovery.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
