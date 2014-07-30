import threading

class NodeCommunicator(threading.Thread):
    
    def __init__(self, server, address, socket):
        self.server = server
        self.address = address
        self.socket = socket

    def run(self):
        self.socket.send(self.job)
        output = self.socket.recv()
        self.server.register_done(self,output)


    def run_job(self, job):
        self.job = job
        self.start()
