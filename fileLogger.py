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