import os

FILE_NAME = "logs/log.txt"
os.makedirs(os.path.dirname(FILE_NAME), exist_ok=True)

def write(text):
    f = open(FILE_NAME, "a") # open in Append mode
    f.write(f"{text}\n")
    f.close()

def read():
    f = open(FILE_NAME, "r") # reads and return entire file
    return f.read()

#DA SISTEMARE (ho fatto un copia-incolla e non ho la minima idea di come funzioni ma funziona)
def getLogs():

    fname = FILE_NAME
    N = 75
     
    # assert statement check
    # a condition
    assert N >= 0
     
    # declaring variable
    # to implement 
    # exponential search
    pos = N + 1
     
    # list to store
    # last N lines
    lines = []
     
    # opening file using with() method
    # so that file get closed
    # after completing work
    with open(fname) as f:
         
        # loop which runs
        # until size of list
        # becomes equal to N
        while len(lines) <= N:
             
            # try block
            try:
                # moving cursor from
                # left side to
                # pos line from end
                f.seek(-pos, 2)
         
            # exception block 
            # to handle any run 
            # time error
            except IOError:
                f.seek(0)
                break
             
            # finally block 
            # to add lines 
            # to list after
            # each iteration
            finally:
                lines = list(f)
             
            # increasing value
            # of variable
            # exponentially
            pos *= 2
             
    # returning the
    # whole list
    # which stores last
    # N lines
    logs = lines[-N:]
    text = ""
    for log in logs:
        text += log
    return text

print(getLogs())