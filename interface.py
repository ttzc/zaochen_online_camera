
def log(function: callable, *args):
    function("".join(str(msg) for msg in args))
    # message = ""
    # for msg in args:
    #     message += str(msg)
    # function(message)


class Task:
    pid = -1
    len = 0
    hash_sha256 = ""


class ClientBase:
    name = ""
    pid = 0
    websocket = None
    task_list = []

    def __init__(self) -> None:
        self.name = ""
        self.pid = 0
        self.websocket = None
        self.task_list = []

    def add_task(self) -> None:
        pass
