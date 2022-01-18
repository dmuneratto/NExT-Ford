
import mysql.connector as connector

cnx = connector.connect(user = 'root', password = '', host = 'localhost', database = 'aula9')

# sistema de concessionaria

cursor = cnx.cursor()

query = ('CREATE TABLE IF NOT EXISTS carro(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, marca TEXT NOT NULL ,modelo TEXT NOT NULL, ano TEXT, valor DECIMAL(10.2))')

cursor.execute(query)   

insert = ('INSERT INTO carro (marca, modelo, ano, valor) VALUES( %s, %s, %s, %s)')

data = ('Ford','Ranger','2022', 100000.00)

cursor.execute(insert, data)

cnx.close()