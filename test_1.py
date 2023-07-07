from http.server import HTTPServer, BaseHTTPRequestHandler
from http import client


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        pass


h1 = client.HTTPConnection('localhost', 8001)
h1.request("GET", "/")

res = h1.getresponse()
print(res.status, res.reason)

data = res.read()
print(data)
