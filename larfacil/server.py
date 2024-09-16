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
