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
                                                                    request["stop"], request["resolution"],
                                                                    main.TYPE.JSON), "utf8"))
        elif request["method"] == "metadata":
            self.wfile.write(bytes(main.get_heightmap_metadata(request["filename"], request["resolution"],
                                                               main.TYPE.JSON), "utf8"))
        elif request["method"] == "voxel":
            self.wfile.write(bytes(main.get_voxel_data(request["filename"], request["start"], request["stop"],
                                                       request["resolution"], request["water_level"], main.TYPE.JSON), "utf8"))
        elif request["method"] == "voxel_metadata":
            self.wfile.write(bytes(main.get_voxel_metadata(request["filename"], request["resolution"], main.TYPE.JSON), "utf8"))


httpd = HTTPServer(('192.168.1.22', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()