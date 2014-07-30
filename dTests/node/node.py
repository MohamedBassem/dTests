import utils.my_socket
import socket
import os
from subprocess import call
import subprocess

class Node:

    def __init__(self, port):
        self.port = port

    def start(self):
        s = utils.my_socket.MySocket()
        s.connect((socket.gethostname(), self.port))
        print "Connected to server on port %s" % self.port
        while True:
            job = s.recv()
            print "New job recieved : %s " % job
            job = json.loads(job)
            self.execute_job(job)
            output = self.finalize_output()
            s.send(output)

    def execute_job(self, job):
        working_directory = "/tmp/dTests_#" + str(job["job_id"])
        os.mkdir(working_directory)
        os.chdir(working_directory)
        
        code = job["source_file"]
        file_name = job["source_file_name"]
        compile_name = file_name.split(".")[:-1][0]
        f = open(file_name,'w')
        f.write(code)
        f.close()
        
        subprocess.call(["/usr/bin/env", "g++", file_name, "-o", compile_name])

        self.outputs = []
        for testcase in job["testcases"]:
            process = subprocess.Popen(["./%s" % compile_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            process.stdin.write(testcase[1])
            process.stdin.close()
            process.wait()
            testcase_output = process.stdout.read()
            self.outputs.append( [testcase[0], testcase_output] )
   
    def finalize_output(self):
        return json.dumps(self.outputs)

