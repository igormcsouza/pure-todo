import os
import json
from http.server import BaseHTTPRequestHandler


class RequestError(Exception):
    pass


class StatusCode:
    OK_200 = 200
    CREATED_201 = 201
    ACCEPTED_202 = 202
    NO_CONTENT_204 = 204
    BAD_REQUEST_400 = 400
    NOT_FOUND_404 = 404
    INTERNAL_SERVER_ERROR_500 = 500


class AppFramework(BaseHTTPRequestHandler):

    TEMPLATE_DIR = 'templates'
    CONTENT_TYPE = {
        "text": "text/plain"
    }

    def _fallback_404(self):
        self.send_response(StatusCode.NOT_FOUND_404)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>404 - Not Found</h1>")

    def _serve_static_files(self) -> bool:
        if self.path.endswith("favicon.ico"):
            self.send_response(200)
            self.send_header('Content-Type', 'image/x-icon')
            self.end_headers()

            with open(
                os.path.join(self.TEMPLATE_DIR, "static", "favicon.ico"), "rb"
            ) as file:
                self.wfile.write(file.read())

            return True

        elif self.path.startswith("/js"):
            self.send_response(200)
            self.send_header("Content-Type", "text/js")
            self.end_headers()

            with open(
                os.path.join(
                    self.TEMPLATE_DIR, "js", self.path.removeprefix("/js/")
                ), "rb"
            ) as js:
                self.wfile.write(js.read())

            return True

        elif self.path.startswith("/css"):
            self.send_response(200)
            self.send_header("Content-Type", "text/css")
            self.end_headers()

            with open(
                os.path.join(
                    self.TEMPLATE_DIR, "css", self.path.removeprefix("/css/")
                ), "rb"
            ) as css:
                self.wfile.write(css.read())

            return True

        else:
            return False

    def _respond_as_html(self, html_path: str):
        self.send_response(StatusCode.OK_200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        with open(os.path.join(self.TEMPLATE_DIR, html_path), "rb") as html:
            self.wfile.write(html.read())

    def _respond_as_json(
            self, json_object: dict, status_code: int = StatusCode.OK_200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        self.wfile.write(json.dumps(json_object).encode('utf-8'))

    def _respond_as_error(
            self, error_msg: str,
            status_code: int = StatusCode.INTERNAL_SERVER_ERROR_500):
        self.send_response(status_code)
        self.send_header("Content-type", self.CONTENT_TYPE["text"])
        self.end_headers()
        self.wfile.write(bytes(error_msg, "utf-8"))

    def _load_json_request(self) -> dict:
        content_length = int(self.headers['Content-Length'])

        # Read the POST data from the request
        post_data = self.rfile.read(content_length)

        # Assuming the POST data is in JSON format
        return json.loads(post_data.decode('utf-8'))
