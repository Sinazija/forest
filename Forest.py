import os
import json
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

PORT = 3000
SOCKET_PORT = 5000
CONTENT_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.jpg': 'image/jpg'
}

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_file('forest.html')
        elif pr_url.path == '/Registr.html':
            self.send_file('Registr.html')
        elif pr_url.path == '/style.css':
            self.send_file('style.css', content_type='text/css')
        elif pr_url.path == '/Logo.jpg':
            self.send_file('Logo.jpg', content_type='image/jpeg')
            
    def do_POST(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/Regisrt':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Отримуємо дані з форми
            data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            username = data.get('username', [''])[0]
            message = data.get('message', [''])[0]
            
            self.send_to_socket_server(username, message)
            
    def send_to_socket_server(self, username, message):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        data = {
            current_time: {
                'username': username,
                'message': message
            }
        }
        json_data = json.dumps(data)
        
        file_path = os.path.join(os.getcwd(), 'storage', 'data.json')
        with open(file_path, 'a+') as f:
            f.seek(0)
            contents = f.read()
            if contents:
                f.seek(0, os.SEEK_END)
                f.write('\n')
            f.write(json_data)
        
    def send_file(self, file_name, content_type=None):
        file_path = os.path.join(os.getcwd(), file_name)
        
        if not os.path.isfile(file_path):
            self.send_error(404, 'File Not Found')
            return
        
        if content_type is None:
            extension = os.path.splitext(file_name)[1]
            content_type = CONTENT_TYPES.get(extension, 'application/octet-stream')
        
        with open(file_path, 'rb') as f:
            content = f.read()
        
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(content)

def run_http_server():
    print('Сервер {3000} запущено')
    http_server = HTTPServer(('', PORT), HttpHandler)
    http_server.serve_forever()

if __name__ == '__main__':
    # Створюємо папку "storage", якщо вона не існує
    os.makedirs('storage', exist_ok=True)

    # Запускаємо HTTP сервер у окремому потоці
    http_thread = threading.Thread(target=run_http_server)
    http_thread.start()