import threading
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

from .danmaku_signal import danmaku_signal


class DualStackServer(HTTPServer):
    address_family = socket.AF_INET6

    def server_bind(self):
        # Explicitly enable dual-stack support by disabling IPV6_V6ONLY
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        super().server_bind()

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
        try:
            # Use '::' to listen on all IPv6 and IPv4 interfaces (Dual Stack)
            self.server = DualStackServer(('::', 19172), RescueHandler)
            print("Rescue API server started on [::]:19172 (Dual Stack)")
            self.server.serve_forever()
        except OSError as e:
            print(f"Error starting Rescue API server: {e}")
            self.server = None

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
