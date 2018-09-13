from http.server import HTTPServer, BaseHTTPRequestHandler
import main
import json


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    # Allow for users to provide parameters for method call
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        request = json.loads(body)

        self.send_response(200)
        self.end_headers()

        if request["method"] == "variable":
            self.wfile.write(bytes(main.get_variable_heightmap_data(request["filename"], request["start"],
                                                                    request["stop"], main.TYPE.JSON), "utf8"))
        elif request["method"] == "metadata":
            self.wfile.write(bytes(main.get_heightmap_metadata(request["filename"], main.TYPE.JSON), "utf8"))


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()