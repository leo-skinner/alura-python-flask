from flask import Flask, render_template, request, redirect, session, flash, url_for
from jogo import Jogo
from usuario import Usuario
from prepara_banco import Prepara_Banco

#inicializa um flask
app = Flask(__name__)
app.secret_key = 'skinner'

#Criando usuários para testar...
u1 = Usuario('leo', 'Leo Skinner', 'leo')
u2 = Usuario('augusto', 'Augusto Skinner', 'java')
u3 = Usuario('isabel', 'Isabel Pimenta', 'bebel')

usuarios = {u1.id: u1, u2.id: u2, u3.id: u3}

lista = []


#indica a rota onde aparecerá a tela.
@app.route('/')
def index():

    #retorna a html e o valor da variavel titulo dentro da html.
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
        #url_for chama o método login e o método novo.
    return render_template('novo.html', titulo='Cadastrar Jogos')


@app.route(
    '/criar', methods=[
        'POST',
    ])
#O método POST deve ser definido, pois o padrão é GET.
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))
    #render_template('lista.html', titulo='jogos', jogos=lista)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route(
    '/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]

        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash(request.form['usuario'] + ' errou a senha.')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado.')
    return redirect(url_for('index'))


app.run(host='0.0.0.0', port=8080, debug=True)  #executa o app.
