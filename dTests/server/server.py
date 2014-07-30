#!/usr/bin/env python

import threading
import utils.my_socket
import socket
import node_communicator
import json
import random

class Server:


    def __init__(self, nodes_port, jobs_port):
        self.nodes_port = nodes_port
        self.jobs_port = jobs_port
        self.nodes = []
        self.job_count = 0

    def listen_node(self):
        s = utils.my_socket.MySocket()
        host = socket.gethostname()
        port = self.nodes_port
        s.bind(host, port)
        print "Node listener started and listening on port %s" % port
        s.listen(5)
        while True:
            client, address = s.accept()
            print 'Node ', address , ' connected to the server'
            new_node = NodeCommunicator(server, address, client)
            self.nodes.append(new_node)
    
    def listen_job(self):
        s = utils.my_socket.MySocket()
        host = socket.gethostname()
        port = self.jobs_port
        print "Job listener started and listening on port %s" % port
        s.bind(host,port)
        s.listen(5)
        while True:
            client, address = s.accept()
            print 'New job is being initiated'
            print 'The new job will run with %s nodes' % len(self.nodes)
            job_description = json.loads(client.recv())
            job_id = random.randrange(1000000000000,10000000000000000)
            print 'Job %s recieved : %s' % (job_id, json.dumps(job_description))
            self.job_count += 1
            node_job_description = {}
            node_job_description["job_id"] = job_id
            node_job_description["source_file_name"] = job_description["source_file"]
            node_job_description["source_file"] = Server.read_code(job_description["source_file"])
            testcases_per_node = (len(job_description["testcases"]) + len(self.nodes) - 1 )/len(self.nodes)
            index = 0
            for node in self.nodes:
                tests = []
                for i in range(0,testcases_per_node):
                    tests.append([index, job_description["testcases"][index]])
                    index += 1
                node_job_description["testcases"] = tests
                node.run_job(json.dumps(node_job_description))
            self.running_nodes = len(self.nodes)
            self.semaphore = threading.Semaphore(0)
            self.semaphore.acquire()
            self.finalize_output()
            client.send(self.output)
            client.close()

    def start(self):
        node_listener = threading.Thread(target=self.listen_node)
        node_listener.daemon = False
        node_listener.start()
        job_listener = threading.Thread(target=self.listen_job)
        job_listener.daemon = False
        job_listener.start()

    def register_done(self, node, output):
        self.partial_outputs += output
        print "Node %s finished its work" % node.getAddress()
        self.running_nodes -= 1
        if not self.running_nodes:
            self.semaphore.release()
            
    def finalize_output(self):
        self.partial_outputs.sort()
        self.output = [ x[1] for x in self.partial_outputs ]
        self.output = "".join([ str(i[1]) for i in self.output ])
    
    def read_code(cls, path):
        content = ''
        with open(path, 'r') as content_file:
            content = content_file.read()
        return content



