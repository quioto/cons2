from flask import Flask, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
from os import path
from bd import *
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Instanciar o objeto MySQL
mysql = MySQL()
# Ligar o MYSQL ao Flask
mysql.init_app(app)

up_folder=('static/images')


config(app)


@app.route('/')
def home():
    conn = mysql.connect()
    cursor = conn.cursor()
    imagens = sql_get_carinfo(cursor, conn)
    return render_template ('home.html',imagens=imagens)


#LOGIN
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/log', methods=['GET','POST'])
def logando():
    if request.method == 'POST':
        login = request.form.get('login')
        senha = request.form.get('senha')
        conn = mysql.connect()
        cursor = conn.cursor()
        idlogin = get_idlogin(cursor, conn, login, senha)
        if idlogin is False:
            return render_template('login.html', erro='verifique o login e a senha')
        else:
            conn = mysql.connect()
            cursor = conn.cursor()
            imagens = get_id_imagens(cursor,conn)
            print(imagens)
            return render_template('controle.html', imagens=imagens)

    else:
        return render_template('login.html', erro='Método incorreto. Use POST!')

#INCLUIR USUARIO
@app.route("/incluir_usuario")
def inserir_usuario():
    return render_template('incluir_usuario.html')

@app.route("/incluir", methods=['POST'])
def incluir(erro=''):
    if request.method == 'POST':
        # recuperar os parametros
        login = request.form.get('login')
        senha = request.form.get('senha')
        if login=='' or senha=='':
            return render_template('incluir_usuario.html', erro='Ensira um login/senha')
        else:
        # Obtendo o cursor para acessar o BD
            conn = mysql.connect()
            cursor = conn.cursor()

            # inserindo o contato
            incluir_cont(cursor, conn, login, senha)

            # Fechar o cursor


            # retornando a lista de contatos
            return render_template('controle.html', erro='Usuário adicionado com sucesso!')
    else:
        incluir()
#EXCLUIR USUÁRIO
@app.route("/excluir_anuncio/<id_imagem>")
def excluir_anuncio(id_imagem):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql_excluir_carro(cursor, conn, id_imagem)
    return redirect(url_for("controle"))


@app.route("/usuario_excluido", methods=['POST'])
def usuario_exluido():
    login = request.form.get('login')
    senha = request.form.get('senha')

    # Obtendo o cursor para acessar o BD
    conn = mysql.connect()
    cursor = conn.cursor()

    # Obtendo o idlogin
    idlogin = get_idlogin(cursor, conn, login, senha)

    # Verificar a senha
    if idlogin is False:
        return render_template('excluir_usuario.html')
    else:
        conn = mysql.connect()
        cursor = conn.cursor()
        print(idlogin)
        return render_template('controle.html')



@app.route("/inserir_anuncio")
def inserir_anuncio():
    return render_template("inserir_anuncio.html")

@app.route('/anuncio_inserido', methods=['GET', 'POST'])
def anuncio_inserido():
    if request.method == 'POST':
        # verifica se tem a parte file no request
        if 'file' not in request.files:
            return render_template('inserir_anuncio.html')

        # pega o arquivo
        arquivo = request.files['file']

        # se o usuario nao selecionar o arquivo
        # o browser manda um arquivo sem nome
        if arquivo.filename == '':
            return render_template('inserir_anuncio.html')
        else:
            nome_arquivo = secure_filename(arquivo.filename)
            if(nome_arquivo.split(".")[1]=="jpg" or nome_arquivo.split(".")[1]=="png"):
                arquivo.save(path.join(up_folder, nome_arquivo))
                conn = mysql.connect()
                cursor = conn.cursor()
                placa = request.form.get('placa')
                modelo = request.form.get('modelo')
                marca = request.form.get('marca')
                valor = request.form.get('valor')
                vip = request.form.get('vip')
                if(placa!="" and modelo!="" and marca!="" and valor!="" and vip!=""):
                    criar_anuncio(cursor,conn,placa,modelo,marca,valor,vip,nome_arquivo)
                    return redirect(url_for("home"))
                else:
                    return render_template('inserir_anuncio.html')
            else:
                return render_template('inserir_anuncio.html')


@app.route("/reservar/<id>")
def reservar(id):
    return render_template("formulario_reserva.html",id=id)


@app.route("/reservado/<id_carro>",  methods=['GET', 'POST'])
def reservado(id_carro):
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        if (nome != "" and cpf != "" and email != ""):
            sql_seta_cliente(cursor, conn, nome, cpf, email)
            conn = mysql.connect()
            cursor = conn.cursor()
            sql_reservar_carro(cursor,conn,id_carro,cpf)
            return redirect(url_for("home"))
        else:
            return render_template("formulario_reserva.html",id=id_carro)
    else:
        return render_template("formulario_reserva.html",id=id_carro)


@app.route("/reservas")
def reservas():
    conn = mysql.connect()
    cursor = conn.cursor()
    imagens = sql_get_carinfo(cursor,conn)
    return render_template("carros_reservados.html",imagens=imagens)

@app.route("/tirar_reserva/<id_carro>")
def tirar_reserva(id_carro):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql_tirareserva_carro(cursor,conn,id_carro)
    conn = mysql.connect()
    cursor = conn.cursor()
    imagens = sql_get_carinfo(cursor, conn)
    return render_template("carros_reservados.html", imagens=imagens)




if __name__ == '__main__':
    app.run(debug=True)


