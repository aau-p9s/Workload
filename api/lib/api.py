from http.server import BaseHTTPRequestHandler
from typing import Any, Callable
from json import loads

from lib.tasks.task import Task

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

        
    def getData(self) -> dict[str, Any]:
        dataSize:int = int(self.headers.get("Content-Length", 0))
        return loads(self.rfile.read(dataSize).decode())

    def ok(self, message:str):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message.encode())


    def matmul(self):
        # request has to be a POST request, so the parameters should be in the body...
        data:dict[str, Any] = self.getData()
        x:int = data["x"]
        y:int = data["y"]
        task = mm(((x, y), (y,x)))
        print(f"running mm with {x=} and {y=}")
        task.run()
        print("finished mm")
        self.ok("finished mm")

    def sum(self):
        data = self.getData()
        size:tuple[int, int] = (data["x"], data["y"])
        task:Task = sumTask(size)
        print("calculating sum...")
        res:Any = task.run()
        self.ok(f"{res}")

    def do_GET(self):
        for path, method, handler in self.handlers:
            if self.path == path and method == "GET":
                handler(self)

    def do_POST(self):
        for path, method, handler in self.handlers:
            if self.path == path and method == "POST":
                handler(self)


