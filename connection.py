import mysql.connector
from mysql.connector import errorcode

class connection:
    def __init__(self, host, user, password, database, port = 3306):
        try:
            self.db_connection = mysql.connector.connect(host=host, user=user, password=password, database=database, port=port)
            self.db_connection
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                return None
            elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return None
            else:
                return error

    def selectUserOuro(self, CodigoContrato):
        cursor = self.db_connection.cursor()
        query = "SELECT NOME AS NomeAluno FROM usuarios WHERE LOGIN = %s GROUP BY LOGIN"
        cursor.execute(query, (CodigoContrato,))
        try:
            user = cursor.fetchone()[0]
            dados = {'NomeAluno' : user}
            return dados
        except:
            return {'NomeAluno':cursor.fetchone()}

    def selectUserPresenca(self, CodigoContrato, DataPresenca, HoraPresenca):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM presencas WHERE CodigoContrato = %s AND DataPresenca = %s AND HoraPresenca = %s GROUP BY CodigoContrato"
        cursor.execute(query, (CodigoContrato,DataPresenca,HoraPresenca,))
        return cursor.fetchone()
    
    def insert(self, dados):
        cursor = self.db_connection.cursor()
        query = """INSERT INTO presencas(CodigoContrato, NomeAluno, DataPresenca, HoraPresenca, DiaSemana, Computador, IpComputador) VALUES(%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (dados["CodigoContrato"], dados['NomeAluno'], dados['DataPresenca'], dados['HoraPresenca'], dados['DiaSemana'], dados['Computador'], dados['IpComputador'],))
        self.db_connection.commit()
        return cursor.rowcount

    def closedb(self):
        self.db_connection.close()

    def selectUserOuroByTheName(self, NomeAluno):
        cursor = self.db_connection.cursor()
        query = "SELECT LOGIN, SENHA FROM usuarios WHERE NOME = %s GROUP BY NOME"
        cursor.execute(query, (NomeAluno,))
        try:
            user = cursor.fetchone()
            dados = {'CodigoContrato' : user[0], 'SenhaAluno' : user[1]}
            return dados
        except:
            return False