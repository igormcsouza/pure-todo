import os
import json
import logging
import argparse
import socketserver
from http.server import BaseHTTPRequestHandler


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


todos = []


class Application(BaseHTTPRequestHandler):

    TEMPLATE_DIR = 'templates'
    CONTENT_TYPE = {
        "text": "text/plain"
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

            with open(os.path.join(self.TEMPLATE_DIR, "index.html"), "rb") as html:
                self.wfile.write(html.read())

        elif self.path == "/get-todos":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            self.wfile.write(json.dumps({"todos": todos}).encode('utf-8'))

        ## Deals with static files and other paths related to the frontend.

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

        ## Fallback

        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 - Not Found</h1>")

    def do_POST(self):
        if self.path == "/add-todo":
            content_length = int(self.headers['Content-Length'])
        
            # Read the POST data from the request
            post_data = self.rfile.read(content_length)
            
            try:
                # Assuming the POST data is in JSON format
                data = json.loads(post_data.decode('utf-8'))
                
                # Process the data
                todos.append(data["todo"])
                
                # Send a response
                self.send_response(201)
                self.send_header("Content-type", self.CONTENT_TYPE["text"])
                self.end_headers()
                self.wfile.write(bytes("Data received and processed", "utf-8"))
                
            except json.JSONDecodeError as e:
                logging.error(f"Error parsing json! {e}")

                # Handle JSON parsing errors
                self.send_response(400)
                self.send_header("Content-type", self.CONTENT_TYPE["text"])
                self.end_headers()
                self.wfile.write(bytes("Invalid JSON data: " + str(e), "utf-8"))

    def do_DELETE(self):
        if self.path.startswith("/remove-todo"):
            remove_todo = self.path.split("/")[-1].replace("%20", " ")

            try:
                todos.remove(remove_todo)

                self.send_response(201)
                self.send_header('Content-type', self.CONTENT_TYPE["text"])
                self.end_headers()
                self.wfile.write(bytes("Data received and processed", "utf-8"))
            except ValueError:
                logging.error(f"There is no todo: {remove_todo}")

                self.send_response(400)
                self.send_header('Content-type', self.CONTENT_TYPE["text"])
                self.end_headers()
                self.wfile.write(bytes(f"Invalid todo: {remove_todo}", "utf-8"))
        

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