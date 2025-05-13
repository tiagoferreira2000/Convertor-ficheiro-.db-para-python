import csv
import mysql.connector
import xml.etree.ElementTree as ET


def carregar_configuracao():
    tree = ET.parse('config.xml')
    root = tree.getroot()

    host = root.find('host').text
    user = root.find('user').text
    password = root.find('password').text
    database = root.find('database').text

    return host, user, password, database


host, user, password, database = carregar_configuracao()

conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
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
