import os

def getAllExtensions(folder):
    extList = []
    for root, dirs, files in os.walk(folder, topdown=True):
        for f in files:
            filename, file_extension = os.path.splitext(f)
            extList.append(file_extension[1:])

    return(set(extList))
