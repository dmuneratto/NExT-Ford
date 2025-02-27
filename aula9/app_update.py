import mysql.connector as connector
# sistema de concessionaria


def connection():
    cnx = connector.connect(user='root', password='',
                            host='localhost', database='aula9')
    return cnx


def create_table(cnx):
    cursor = cnx.cursor()
    query = ('CREATE TABLE IF NOT EXISTS carro(\
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, \
    marca TEXT NOT NULL, \
    modelo TEXT NOT NULL, \
    ano TEXT, \
    valor DECIMAL(10,2)\
    )')
    cursor.execute(query)


def insert_car(cnx, car):
    cursor = cnx.cursor()
    insert = ('INSERT INTO carro(marca, modelo, ano, valor) VALUES(%s, %s, %s, %s)')
    data = (car['marca'], car['modelo'], car['ano'], car['valor'])
    cursor.execute(insert, data)
    cnx.commit()

def update_car(cnx,car):
    cursor = cnx.cursor()
    update = ('UPDATE carro SET marca = %s, modelo = %s, ano = %s, valor =%s WHERE id = %s')
    data = (car['marca'], car['modelo'], car['ano'], car['valor'], car['id'])
    cursor.execute(update,data)
    cnx.commit()

def delete_car(cnx, car):
    cursor = cnx.cursor()
    delete = ('DELETE FROM carro WHERE id = %s')
    data = (car['id'])
    cursor.execute(delete,data)
    cnx.commit()


def lista_carros(cnx):
    cursor = cnx.cursor()
    query = ('select * from carro')
    cursor.execute(query)
    return list(cursor)


def desconnect(cnx):
    cnx.close()


if __name__ == '__main__':
    connector = connection()
    create_table(connector)
    # marca = input('Digite a marca do carro: ')
    # modelo = input('Digite a modelo do carro: ')
    # ano = input('Digite a ano do carro: ')
    # valor = input('Digite a valor do carro: ')
    id = input('Digite o id: ')
    # insert_car(connector, {
    #   'marca': marca,
    #   'modelo': modelo,
    #   'ano': ano,
    #   'valor': valor
      
    # })

    # update_car(connector, {
    #   'marca': marca,
    #   'modelo': modelo,
    #   'ano': ano,
    #   'valor': valor,
    #   'id': id
    # })
    delete_car(connector,{'id':id})
    print(lista_carros(connector))
    desconnect(connector)
