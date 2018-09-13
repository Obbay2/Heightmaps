from http.server import HTTPServer, BaseHTTPRequestHandler
import main


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Write content as utf-8 data
        self.wfile.write(bytes(main.get_variable_heightmap_data("heightmap.png", 0, 3, main.TYPE.JSON), "utf8"))


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()