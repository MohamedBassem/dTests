def compile_file(file_name, lang):
    if lang == "cpp":
        compile_name = ".".join(file_name.split(".")[:-1])
        subprocess.call(["/usr/bin/env", "g++", file_name, "-o", compile_name])
    elif lang == "java":
        subprocess.call(["/usr/bin/env", "javac", file_name])

def exec_file(file_name, lang, stdin=None):
    compile_name = ".".join(file_name.split(".")[:-1])
    output = ""
    if lang == "cpp":
        process = subprocess.Popen(["./%s" % compile_name], stdin= ( None if not stdin else subprocess.PIPE ) , stdout=subprocess.PIPE)
        if not stdin:
            process.stdin.write(stdin)
            process.stdin.close()
        process.wait()
        output = process.stdout.read()
    elif lang == "java":
        process = subprocess.Popen(["/usr/bin/env", "java", compile_name], stdin= ( None if not stdin else subprocess.PIPE ) , stdout=subprocess.PIPE)
        if not stdin:
            process.stdin.write(stdin)
            process.stdin.close()
        process.wait()
        output = process.stdout.read()
    return output
