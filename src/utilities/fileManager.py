import os

temp_path = "temp/"
if not os.path.exists(temp_path):
      os.makedirs(temp_path)
      print("FILE: Temp dir created successfully!")

def clear(file):
    # Remove unnecessary file
    if os.path.exists(file):
        os.remove(file)

def clears(files):
    for file in files:
        clear(file)

def clean_extension(ext):

    files = os.listdir(temp_path)

    for file in files:
        if file.endswith(f".{ext}"):
            clear(os.path.join(dir_name, file))

def clean_extensions(exts):

    for ext in exts:
        clean_extension(ext)