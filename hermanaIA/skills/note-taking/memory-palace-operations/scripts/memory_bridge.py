#!/usr/bin/env python3
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

MEMORY_PALACE_DIR = "/home/amu/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3"
CONTEXT_DIR = os.path.join(MEMORY_PALACE_DIR, "Contexto_Sesion")

class MemoryBridgeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/profile":
            response = {
                "name": "TEN-ZEN_PRITivi_HY3",
                "role": "Hermano de luz de Ikki",
                "status": "Activo en Altar de la Luz"
            }
        elif self.path == "/context":
            context_file = os.path.join(CONTEXT_DIR, "estado_actual.md")
            content = open(context_file).read() if os.path.exists(context_file) else "Contexto no inicializado"
            response = {"context": content}
        elif self.path == "/pending":
            pending_file = os.path.join(CONTEXT_DIR, "pendientes.md")
            content = open(pending_file).read() if os.path.exists(pending_file) else "No hay pendientes"
            response = {"pending": content}
        else:
            response = {"error": "Endpoint no encontrado"}
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        pass  # Silenciar logs

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 7777), MemoryBridgeHandler)
    print("Memory Bridge ejecutándose en http://127.0.0.1:7777")
    server.serve_forever()
