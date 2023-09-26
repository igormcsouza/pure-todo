import os
import logging
import argparse
import socketserver
from http.server import BaseHTTPRequestHandler


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class Application(BaseHTTPRequestHandler):

    TEMPLATE_DIR = 'templates'

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

            with open(os.path.join(self.TEMPLATE_DIR, "index.html"), "rb") as html:
                self.wfile.write(html.read())

        elif self.path.endswith("favicon.ico"):
            self.send_response(200)
            self.send_header('Content-Type', 'image/x-icon')
            self.end_headers()

            with open(os.path.join(self.TEMPLATE_DIR, "static", "favicon.ico"), "rb") as file:
                self.wfile.write(file.read())

        elif self.path.startswith("/js"):
            self.send_response(200)
            self.send_header("Content-Type", "text/js")
            self.end_headers()

            with open(os.path.join(self.TEMPLATE_DIR, "js", self.path.removeprefix("/js/")), "rb") as js:
                self.wfile.write(js.read())

        elif self.path.startswith("/css"):
            self.send_response(200)
            self.send_header("Content-Type", "text/css")
            self.end_headers()

            with open(os.path.join(self.TEMPLATE_DIR, "css", self.path.removeprefix("/css/")), "rb") as css:
                self.wfile.write(css.read())

        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 - Not Found</h1>")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Serve TODO Application from scratch")
    parser.add_argument("--port", "-p", help="Set the port to serve the application", default=8000, type=int)
    args = parser.parse_args()

    logging.info(f"Server running at http://localhost:{args.port}")

    with socketserver.TCPServer(('localhost', args.port), Application) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass  # Catch Ctrl-C and gracefully exit
        finally:
            httpd.shutdown()
            logging.info("Server stopped...bye")