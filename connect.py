import csv
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",      # Tu nombre de usuario de MySQL
    password="root",  # Tu contraseña de MySQL
    database="gestor"  # Nombre de la base de datos a la que deseas conectarte
)

cursor = conn.cursor()


cursor.execute("""
    SELECT pedidos.idpedidos, pedidos.idusuario, usuarios.nome AS nome_usuario, pedidos.idproduto, produtos.descricao AS descricao_produto, pedidos.data, pedidos.quantidade         
    FROM pedidos
    JOIN usuarios ON pedidos.idusuario = usuarios.idusuario
    JOIN produtos ON pedidos.idproduto = produtos.idproduto
""")


dados = cursor.fetchall()


colunas = [descricao[0] for descricao in cursor.description]


with open('gestor.csv', 'w', encoding='utf-8') as ficheiro_csv:
    escritor_csv = csv.writer(ficheiro_csv)
    escritor_csv.writerow(colunas)
    escritor_csv.writerows(dados)


conn.close()

print("Ficheiro CSV criado com sucesso!")
