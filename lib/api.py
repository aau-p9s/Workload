from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Callable
from json import loads

from .tasks.sum import sumTask

from .tasks.mm import mm

class Server(BaseHTTPRequestHandler):
    handlers:list[tuple[str, str, Callable]] = [
        ("/", "GET", lambda server: server.ok("got request...")),
        ("/mm", "POST", lambda server: server.matmul()),
        ("/sum", "POST", lambda server: server.sum())
    ]
    

    def __init__(self, request, client_address, server) -> None:
        super().__init__(request, client_address, server)

        
    def getData(self):
        dataSize = int(self.headers.get("Content-Length", 0))
        return loads(self.rfile.read(dataSize).decode())

    def ok(self, message:str):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message.encode())


    def matmul(self):
        # request has to be a POST request, so the parameters should be in the body...
        data = self.getData()
        x, y = data["x"], data["y"]
        task = mm(((x, y), (y,x)))
        print(f"running mm with {x=} and {y=}")
        task.run()
        print("finished mm")
        self.ok("finished mm")

    def sum(self):
        data = self.getData()
        x, y = data["x"], data["y"]
        task = sumTask((x, y))
        print("calculating sum...")
        res = task.run()
        self.ok(f"{res}")

    def do_GET(self):
        for path, method, handler in self.handlers:
            if self.path == path and method == "GET":
                handler(self)

    def do_POST(self):
        for path, method, handler in self.handlers:
            if self.path == path and method == "POST":
                handler(self)




if __name__ == "__main__":
    http = HTTPServer(("localhost", 8000), Server)
    http.serve_forever()
    
