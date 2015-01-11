# coding: utf-8

import SocketServer
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Jessica Yuen
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    CONTENT_DIR = "www"

    def handle(self):
        """Handles common (but not all) HTTP requests."""
        # Parse the HTTP request
        self.data = self.request.recv(1024).strip()
        http_request = self.data.splitlines()
        request_line = http_request[0].split()
        path = os.path.abspath(self.CONTENT_DIR + request_line[1]);

        response = None

        # Are we in the www directory?
        if os.path.abspath(self.CONTENT_DIR) not in os.path.realpath(path):
            response = self.response_not_found()

        # Is the path a directory and does index exists?
        elif os.path.isdir(path) and os.path.isfile(path + "/index.html"):
            response = self.response_ok(path + "/index.html", "text/html")

        # Is the path a valid file?
        elif os.path.isfile(path):
            content_type = path.split(".")[-1].lower()
            response = self.response_ok(path, "text/%s" % content_type)

        # Path does not exist
        else:
            response = self.response_not_found()

        # Finally, send in the response!
        self.request.sendall(response)

    def response_ok(self, path, content_type):
        """Returns a simplified HTTP/1.1 200 OK response."""
        return ("HTTP/1.1 200 OK\r\n" +
                "Content-Type: %s\r\n" % content_type +
                open(path).read());

    def response_not_found(self):
        """Returns a simplified HTTP/1.1 404 Not Found response."""
        return ("HTTP/1.1 404 Not Found\r\n" +
                "Content-Type: text/html\n\n" +
                "<!DOCTYPE html>\n" +
                "<html><body><h1>Oops! The page you are looking for seems to " +
                "be missing.</h1></body></html>")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
