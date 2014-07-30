#!/usr/bin/env python

import threading
import socket
import server.node_communicator
import json

class Server:


    def __init__(self, nodes_port, jobs_port):
        self.nodes_port = nodes_port
        self.jobs_port = jobs_port
        self.nodes = []
        self.job_count

    def listen_node(self):
        s = socket.socket()
        host = socket.gethostname()
        port = self.nodes_port
        s.bind((host, port))
        s.listen(5)
        while True:
            client, address = s.accept()
            print 'Node ', address , ' connected to the server'
            new_node = NodeCommunicator(server, address, client)
            nodes.append(new_node)
            new_node.start()
    
    def listen_job(self):
        s = socket.socket()
        host = sockent.gethostname()
        port = self.jobs_port
        s.bind((host,port))
        s.listen(5)
        while True:
            client, address = s.accept()
            print 'New job is being initiated'
            print 'The new job will run with %s nodes' % len(self.nodes)
            job_description = json.loads(socket.recv(2))
            print 'Job recieved : %s' % str(job_description)
            self.job_count += 1
            node_job_description = {}
            node_job_description["source_file"] = Server.read_code(job_description["source_file"])
            node_job_description["language"] = job_description["language"]
            testcases_per_node = (len(job_description["testcases"]) + len(self.nodes) - 1 )/len(self.nodes)
            index = 0
            for node in self.nodes:
                tests = []
                for i in range(0,testcases_per_node):
                    tests.append((index, job_description["testcases"][index]))
                    index += 1
                node_job_description["testcases"] = tests
                node.run_job(str(node_job_description))
            self.running_nodes = len(self.nodes)
            self.semaphore = threading.Semaphore(0)
            self.semaphore.acquire()
            client.send(self.output)
            client.close()

    def start(self):
        node_listener = threading.Thread(target=listen_node)
        node_listener.daemon = True
        node_listener.start()
        job_listener = threading.Thread(target=listen_job)
        job_listener.daemon = True
        job_listener.start()
    
    def read_code(cls, path):
        content = ''
        with open(path, 'r') as content_file:
            content = content_file.read()
        return content



