import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from .danmaku_signal import danmaku_signal

class RescueHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/rescue':
            danmaku_signal.rescue_signal.emit()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Rescue signal sent')
        else:
            self.send_response(404)
            self.end_headers()

class RescueAPI(threading.Thread):
    def __init__(self):
        super().__init__()
        self.server = None

    def run(self):
        self.server = HTTPServer(('0.0.0.0', 19172), RescueHandler)
        print("Rescue API server started on 0.0.0.0:19172")
        self.server.serve_forever()

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
