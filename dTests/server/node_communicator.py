import threading
import json

class NodeCommunicator:
    
    def __init__(self, server, address, socket):
        self.server = server
        self.address = address
        self.socket = socket

    def run(self):
        self.socket.send(self.job)
        output = self.socket.recv()
        output = json.loads(output)
        self.server.register_done(self, output)


    def run_job(self, job):
        self.job = job
        threading.Thread(target=self.run).start()

    def get_address(self):
        return self.address
