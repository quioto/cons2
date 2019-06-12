def config(app):
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
    app.config['MYSQL_DATABASE_DB'] = 'concessionaria'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    app.config['DEBUG'] = True


def sql_excluir_usuario(cursor, conn, idusuario):
    cursor.execute(f'delete from concessionaria.user where idusuario = {idusuario}')
    conn.commit()
    cursor.close()
    conn.close()

def sql_get_carinfo(cursor, conn):
    cursor.execute(f'select idcarros, foto, vip, comprado, reservado, modelo, marca, valor from concessionaria.carros')
    id_imagens = cursor.fetchall()
    cursor.close()
    conn.close()
    return id_imagens

def get_idlogin(cursor, conn, login, senha):
    # Executar o sql
    cursor.execute(f'select idusuario from concessionaria.user where login = "{login}" and senha = "{senha}"')

    # Recuperando o retorno do BD
    idlogin = cursor.fetchone()

    # Fechar o cursor
    cursor.close()
    conn.close()
    if idlogin == None:
        return False
    else:
        return idlogin[0]


def incluir_cont(cursor, conn, login, senha):
    cursor.execute(f'insert into concessionaria.user (login, senha) values("{login}", "{senha}")')
    conn.commit()
    cursor.close()
    conn.close()


def get_id_imagens(cursor,conn):
    cursor.execute(f'select idcarros, foto, vip from concessionaria.carros')
    id_imagens = cursor.fetchall()
    id_imagens = [list(x) for x in id_imagens]
    cursor.close()
    conn.close()
    return id_imagens


def sql_excluir_carro(cursor,conn,idcarros):
    cursor.execute(f'delete from concessionaria.carros where idcarros = {idcarros}')
    conn.commit()
    cursor.close()
    conn.close()




def criar_anuncio(cursor,conn,placa,modelo,marca,valor,vip,foto):
    cursor.execute(f'insert into concessionaria.carros (placa,modelo,marca,valor,vip,foto) values("{placa}", "{modelo}", "{marca}"'
                   f', "{valor}", "{vip}","{foto}")')
    conn.commit()
    cursor.close()
    conn.close()


def sql_get_idlogin(cursor, conn, login, senha):
    # Executar o sql
    cursor.execute(f'select idusuario from concessionaria.user where login = "{login}" and senha = "{senha}"')

    # Recuperando o retorno do BD
    idlogin = cursor.fetchone()

    # Fechar o cursor
    cursor.close()
    conn.close()
    if idlogin == None:
        return False
    else:
        return idlogin[0]


def sql_incluir_cont(cursor, conn, login, senha):
    cursor.execute(f'insert into concessionaria.user (login, senha) values("{login}", "{senha}")')
    conn.commit()
    cursor.close()
    conn.close()



def sql_criar_anuncio(cursor, conn, placa, modelo, marca, valor, vip, foto):
    cursor.execute(f'insert into concessionaria.carros (placa,modelo,marca,valor,vip,foto) values("{placa}", "{modelo}", "{marca}"'
                   f', "{valor}", "{vip}","{foto}")')
    conn.commit()
    cursor.close()
    conn.close()


def sql_atualizar_carro(cursor, conn, idcarros, placa, modelo, marca, valor, vip, foto):
    cursor.execute(f'UPDATE concessionaria.cars SET placa="{placa}", modelo="{modelo}", marca="{marca}", valor="{valor}"'
                   f', vip="{vip}", foto="{foto}" WHERE idcarros = {idcarros}')
    conn.commit()
    cursor.close()
    conn.close()


def sql_setar_carro_vip(cursor, conn, idcarros):
    cursor.execute(f'UPDATE concessionaria.carros SET vip="{1}" WHERE idcarros = {idcarros}')
    conn.commit()
    cursor.close()
    conn.close()


def sql_setar_carro_normal(cursor, conn, idcarros):
    cursor.execute(f'UPDATE concessionaria.carros SET vip="{0}" WHERE idcarros = {idcarros}')
    conn.commit()
    cursor.close()
    conn.close()


def sql_reservar_carro(cursor,conn,idcarros,cpf):
    cursor.execute(f'UPDATE concessionaria.carros SET reservado="{1}", idcomprador="{cpf}" WHERE idcarros = {idcarros}')
    conn.commit()
    cursor.close()
    conn.close()


def sql_tirareserva_carro(cursor,conn,idcarros):
    cursor.execute(f'UPDATE concessionaria.carros SET reservado="{0}", idcomprador="{0}" WHERE idcarros = {idcarros}')
    conn.commit()
    cursor.close()
    conn.close()


def sql_seta_cliente(cursor,conn,nome,cpf,email):
    cursor.execute(f'INSERT into concessionaria.client (nome,cpf,email) VALUES("{nome}", "{cpf}", "{email}")')
    conn.commit()
    cursor.close()
    conn.close()