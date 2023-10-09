from flask import Flask, render_template, request, redirect, session, flash, url_for


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


jogo1 = Jogo('Forza', 'Corrida', 'Xbox')
jogo2 = Jogo('Mortal Kombat', 'Luta', 'Mega Drive')
jogo3 = Jogo('Battlefield', 'Tiro', 'PC')
jogo4 = Jogo('Sonic 2', 'Aventura', 'Master System')
lista = [jogo1, jogo2, jogo3, jogo4]


class Usuario:
    def __init__(self, nome, apelido, senha):
        self.nome = nome
        self.apelido = apelido
        self.senha = senha

usuario1 = Usuario("Fabiana Marques", "Fa", "2700")
usuario2 = Usuario("Fabio Monteiro", "Fabinho", "2413")
usuario3 = Usuario("Frederico Silva", "Fred", "1234")

# dicionario para verificação através da chave 'apelido'
usuarios = {usuario1.apelido: usuario1,
            usuario2.apelido: usuario2,
            usuario3.apelido: usuario3}

# instância do flask
app = Flask(__name__)
app.secret_key = 'chave'  # A secret_key fornece um nível de assinatura criptográfica aos cookies


# criar uma rota
@app.route('/')
# ao criar uma rota, precisa ter uma função para definir o que existe nessa rota
def index():
    # o flask já espera que o arquivo html esteja dentro de um diretório chamado 'templates'
    # o render_template é um helper que permite enviar variáveis do python ao html
    return render_template('lista.html', titulo='Jogos', jogos=lista)


# nova página
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')


# a página criar é uma página de meio termo, apenas uma rota para processar as informações do formulário
# usamos o redirect para redirecionar para a página inicial

@app.route('/criar',
           methods=['POST', ])  # explicitar em lista o método POST, pois por padrão o route aceita apenas o método GET
def criar():
    # request é um helper do flask que pega as informações de nome, categoria e console, através da tag 'name'
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    # instanciar um objeto
    jogo = Jogo(nome, categoria, console)
    # no python, append adiciona item na lista
    lista.append(jogo)  # no python, append adiciona item na lista

    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Login', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.apelido
            # mostra mensagem na tela
            flash(usuario.apelido + ' logado com sucesso')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('index'))


# chama o método run
app.run(debug=True)

# host e porta específicos (não usar para produção), serve para ajudar no ambiente de desenvolvimento
# app.run(host='0.0.0.0', port=8080)
