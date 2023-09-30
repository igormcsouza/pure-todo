import json
import logging
import argparse
import socketserver

from src.repository import TodoRepository
from src.app_framework import AppFramework, StatusCode, RequestError


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class Application(AppFramework):

    def do_GET(self):
        if self.path == "/":
            self._respond_as_html("index.html")

        elif self.path == "/get-todos":
            todos = TodoRepository.get_all()
            self._respond_as_json({"todos": todos})

        ## Deals with static files and other paths related to the frontend.
        elif self._serve_static_files():
            logging.info(f"Served static files at {self.path}")

        ## Fallback

        else:
            self._fallback_404()

    def do_POST(self):
        if self.path == "/add-todo":
            try:
                # Load the request parameters
                data = self._load_json_request()

                if "todo" not in data:
                    raise RequestError(
                        f"There is no todo on the request: {data}")

                # Process the data
                TodoRepository.create(data["todo"])

                # Send a response
                self._respond_as_json(
                    {"response": "Data received and processed"},
                    StatusCode.CREATED_201
                )

            except (json.JSONDecodeError, RequestError) as e:
                logging.error(f"Error parsing json! {e}")

                # Handle JSON parsing errors
                self._respond_as_error(
                    f"Invalid JSON data: {e}", StatusCode.BAD_REQUEST_400)

        ## Fallback

        else:
            self._fallback_404()

    def do_DELETE(self):
        if self.path.startswith("/remove-todo"):
            remove_todo = self.path.split("/")[-1].replace("%20", " ")

            try:
                # Uses the repository to delete the item
                TodoRepository.delete(remove_todo)

                if remove_todo == "":
                    raise RequestError("There is no todo on the request")

                self._respond_as_json(
                    {"response": "Data received and processed"},
                    StatusCode.ACCEPTED_202
                )

            except ValueError:
                logging.error(f"There is no todo: {remove_todo}")

                self._respond_as_error(
                    f"Invalid todo: {remove_todo}", StatusCode.BAD_REQUEST_400)

        ## Fallback

        else:
            self._fallback_404()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Serve TODO Application from scratch")
    parser.add_argument(
        "--port", "-p", help="Set the port to serve the application",
        default=8000, type=int
    )
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
