import os

def clear(file):
    # Remove unnecessary file
    if os.path.exists(file):
        os.remove(file)

def clears(files):
    for file in files:
        clear(file)

def clean_extension(ext):

    dir_name = "temp/"
    files = os.listdir(dir_name)

    for file in files:
        if file.endswith(f".{ext}"):
            clear(os.path.join(dir_name, file))

def clean_extensions(exts):

    for ext in exts:
        clean_extension(ext)