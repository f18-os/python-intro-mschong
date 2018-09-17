#! /usr/bin/env python3

import os, sys, time, re

pid = os.getpid()               # get and remember pid

os.write(1, ("About to fork (pid=%d)\n" % pid).encode())
inp = ""
#rc = os.fork()



while(inp != 'exit'):
    inp = input("$ ")
    rc = os.fork()
    argss = inp.split(" ")
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
        
    elif rc == 0:                   # child
        if argss[len(argss)-2] == '>':
            os.close(1)                 # redirect child's stdout
            sys.stdout = open(argss[len(argss)-1], "w+")
            fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
            os.set_inheritable(fd, True)
            
            for dir in re.split(":", os.environ['PATH']): # try each directory in path
                program = "%s/%s" % (dir, argss[0])
                try:
                    os.execve(program, argss[0:len(argss)-2], os.environ) # try to exec program
                except FileNotFoundError:             # ...expected
                    pass                              # ...fail quietly 
                
            os.write(2, ("Child:    Error: Could not exec %s\n" % argss[0]).encode())
            sys.exit(1)                 # terminate with error
                
        elif argss[len(argss)-2] == '<':
            os.close(0)                 # redirect child's stdout
            sys.stdin = open(argss[len(argss)-1], "r")
            fd = sys.stdin.fileno() # os.open("p4-output.txt", os.O_CREAT)
            os.set_inheritable(fd, True)
                        
            for dir in re.split(":", os.environ['PATH']): # try each directory in path
                program = "%s/%s" % (dir, argss[0])
                try:
                    os.execve(program, argss[1:len(argss)-1], os.environ) # try to exec program
                except FileNotFoundError:             # ...expected
                    pass                              # ...fail quietly 
                
            os.write(2, ("Child:    Error: Could not exec %s\n" % argss[0]).encode())
            sys.exit(1)                 # terminate with error
            
            
        else:
            for dir in re.split(":", os.environ['PATH']): # try each directory in path
                program = "%s/%s" % (dir, argss[0])
                try:
                    os.execve(program, argss, os.environ) # try to exec program
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

