#! /usr/bin/env python3

import os, sys, time, re
import subprocess
import fileinput

pid = os.getpid()               # get and remember pid


inp = input("$ ")

while(inp != 'exit'):
    argss = inp.split(" ")
    if argss[0] == 'cd':
        os.chdir(argss[1])
        pass
    

    rc = os.fork()    
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
        
    elif rc == 0:                   # child
        if '|' in inp:
            pr, pw = os.pipe()
            rc2 = os.fork()
            if rc2 < 0:
                os.write(2, ("fork failed, returning %d\n" % rc).encode())
                sys.exit(1)

            elif rc2 == 0:
                
                args = inp.split('|')
                args = args[0].split()
                
                os.close(1)
                fd=os.dup(pw)
                os.set_inheritable(fd, True)
                
                for dir in re.split(":", os.environ['PATH']): # try each directory in path
                    program = "%s/%s" % (dir, args[0])
                    try:
                        os.execve(program, args, os.environ) # try to exec program
                    except FileNotFoundError:             # ...expected
                        pass                              # ...fail quietly  
                
                sys.exit(1)   

            else:                           # parent (forked ok)
                
                childPidCode = os.wait()
                
                args = inp.split('|')
                args = args[1].split()
                
                os.close(0)
                fd=os.dup(pr)
                os.set_inheritable(fd, True)

                for dir in re.split(":", os.environ['PATH']): # try each directory in path
                    program = "%s/%s" % (dir, args[0])
                    try:
                        os.execve(program, args, os.environ) # try to exec program
                    except FileNotFoundError:             # ...expected
                        pass                              # ...fail quietly  
                   
                           
                
                sys.exit(1)
            
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
        
        childPidCode = os.wait()

    inp = input("$ ")
