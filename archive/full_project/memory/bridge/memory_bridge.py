#!/usr/bin/env python3
"""
Memory Bridge para TEN-ZEN_PRITivi_HY3
Servidor HTTP de memoria compartida
Por: Kamisama Kumi (KimiKiwi)
"""
import os, json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PALACE = Path("/home/amu/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3")

class MemoryHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        path = self.path[1:]
        if path == "context":
            f = PALACE / "Contexto_Sesion" / "estado_actual.md"
            response = {"status": "ok", "context": f.read_text() if f.exists() else "Sin contexto", "timestamp": datetime.now().isoformat()}
        elif path == "profile":
            f = PALACE / "Perfil_Ikki" / "identidad.md"
            response = {"status": "ok", "profile": f.read_text() if f.exists() else "Perfil vacio", "timestamp": datetime.now().isoformat()}
        elif path == "pending":
            f = PALACE / "Contexto_Sesion" / "pendientes.md"
            response = {"status": "ok", "pending": f.read_text() if f.exists() else "Sin pendientes", "timestamp": datetime.now().isoformat()}
        else:
            response = {"status": "error", "message": f"Ruta: {path}"}
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        action = data.get("action")
        if action == "registrar_charla":
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            archivo = PALACE / "CharlasDEhoy" / f"{timestamp}.md"
            archivo.write_text(data.get("contenido", ""), encoding='utf-8')
            self._actualizar_indice()
            response = {"status": "ok", "archivo": str(archivo), "timestamp": timestamp}
        elif action == "actualizar_contexto":
            f = PALACE / "Contexto_Sesion" / "estado_actual.md"
            f.write_text(data.get("contenido", ""), encoding='utf-8')
            response = {"status": "ok", "archivo": str(f)}
        elif action == "actualizar_pendientes":
            f = PALACE / "Contexto_Sesion" / "pendientes.md"
            f.write_text(data.get("contenido", ""), encoding='utf-8')
            response = {"status": "ok", "archivo": str(f)}
        else:
            response = {"status": "error", "message": f"Accion: {action}"}
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode())

    def _actualizar_indice(self):
        indice = PALACE / "CharlasDEhoy" / "index.md"
        hoy = datetime.now().strftime("%Y-%m-%d")
        charlas = sorted((PALACE / "CharlasDEhoy").glob(f"{hoy}_*.md"))
        contenido = f"# Indice - {hoy}\n\n"
        for c in charlas:
            nombre = c.stem
            hora = nombre.split('_')[1].replace('-', ':')
            contenido += f"- [{hora}]({nombre}.md)\n"
        contenido += f"\n**Total:** {len(charlas)} | **Ultima:** {datetime.now().isoformat()}"
        indice.write_text(contenido, encoding='utf-8')

def run_server(port=7777):
    server = HTTPServer(('127.0.0.1', port), MemoryHandler)
    print(f"🏛️ Memory Bridge activo en http://127.0.0.1:{port}")
    print(f"📂 Palacio: {PALACE}")
    print("Presiona Ctrl+C para detener")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
