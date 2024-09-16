import json
import MySQLdb
from http.server import BaseHTTPRequestHandler, HTTPServer

def connect_db():
    connection = MySQLdb.connect(
        host="localhost",
        user="seu_usuario",
        passwd="sua_senha",
        db="larfacil"
    )
    return connection

class MyServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path == '/imoveis':
            self._set_headers()
            self.wfile.write(json.dumps(listar_imoveis()).encode('utf-8'))

def listar_imoveis():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM imoveis")
    rows = cursor.fetchall()
    imoveis = [{"id": row[0], "descricao": row[1], "endereco": row[2], "valor_aluguel": row[3]} for row in rows]
    db.close()
    return imoveis

if __name__ == "__main__":
    webServer = HTTPServer(('localhost', 8080), MyServer)
    print("Servidor rodando na porta 8080...")
    webServer.serve_forever()


import json
import MySQLdb
from http.server import BaseHTTPRequestHandler, HTTPServer

def connect_db():
    """Estabelece a conexão com o banco de dados MySQL."""
    connection = MySQLdb.connect(
        host="localhost",
        user="seu_usuario",
        passwd="sua_senha",
        db="larfacil"
    )
    return connection

class MyServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        """Define os cabeçalhos HTTP para a resposta."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        """Lida com requisições GET e retorna dados em formato JSON."""
        if self.path == '/imoveis':
            self._set_headers()
            self.wfile.write(json.dumps(listar_imoveis()).encode('utf-8'))
        elif self.path == '/locadores':
            self._set_headers()
            self.wfile.write(json.dumps(listar_locadores()).encode('utf-8'))
        elif self.path == '/locatarios':
            self._set_headers()
            self.wfile.write(json.dumps(listar_locatarios()).encode('utf-8'))
        elif self.path.startswith('/aluguel'):
            imovel_id = self.path.split('/')[-1]  # Obtém o ID do imóvel da URL
            self._set_headers()
            self.wfile.write(json.dumps(listar_aluguel(imovel_id)).encode('utf-8'))

def listar_imoveis():
    """Lista todos os imóveis disponíveis no banco de dados."""
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT imoveis.id, imoveis.descricao, imoveis.endereco, imoveis.valor_aluguel, locador.nome
        FROM imoveis
        JOIN locador ON imoveis.locador_id = locador.id
    """)
    rows = cursor.fetchall()
    imoveis = [
        {"id": row[0], "descricao": row[1], "endereco": row[2], "valor_aluguel": row[3], "locador": row[4]}
        for row in rows
    ]
    db.close()
    return imoveis

def listar_locadores():
    """Lista todos os locadores cadastrados no banco de dados."""
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM locador")
    rows = cursor.fetchall()
    locadores = [{"id": row[0], "nome": row[1], "email": row[2], "telefone": row[3]} for row in rows]
    db.close()
    return locadores

def listar_locatarios():
    """Lista todos os locatários cadastrados no banco de dados."""
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM locatario")
    rows = cursor.fetchall()
    locatarios = [{"id": row[0], "nome": row[1], "email": row[2], "telefone": row[3], "status_aluguel": row[4]} for row in rows]
    db.close()
    return locatarios

def listar_aluguel(imovel_id):
    """Lista os locatários que estão alugando um imóvel específico."""
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT locatario.id, locatario.nome, aluguel.data_inicio, aluguel.data_fim
        FROM aluguel
        JOIN locatario ON aluguel.locatario_id = locatario.id
        WHERE aluguel.imovel_id = %s
    """, (imovel_id,))
    rows = cursor.fetchall()
    alugueis = [
        {"locatario_id": row[0], "nome_locatario": row[1], "data_inicio": row[2], "data_fim": row[3]}
        for row in rows
    ]
    db.close()
    return alugueis

if __name__ == "__main__":
    webServer = HTTPServer(('localhost', 8080), MyServer)
    print("Servidor rodando na porta 8080...")
    webServer.serve_forever()
