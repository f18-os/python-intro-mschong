#! /usr/bin/env python3

import os, sys, time, re

pid = os.getpid()               # get and remember pid

os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

rc = os.fork()
argss = sys.argv[1].split(" ")
for arg in argss:
    print(arg)
if rc < 0:
    os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

elif rc == 0:                   # child
    if argss[len(argss)-2] == '>':
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
                     (os.getpid(), pid)).encode())

        os.close(1)                 # redirect child's stdout
        sys.stdout = open(argss[len(argss)-1], "w+")
        fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
        os.set_inheritable(fd, True)
        os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

        for dir in re.split(":", os.environ['PATH']): # try each directory in path
            program = "%s/%s" % (dir, argss[0])
            try:
                os.execve(program, argss[0:len(argss)-2], os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly 

        os.write(2, ("Child:    Error: Could not exec %s\n" % argss[0]).encode())
        sys.exit(1)                 # terminate with error


        

else:                           # parent (forked ok)
    os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                 (pid, rc)).encode())
    childPidCode = os.wait()
    os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                 childPidCode).encode())
