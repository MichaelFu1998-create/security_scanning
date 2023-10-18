def forwardSlash(listOfFiles):
    """convert silly C:\\names\\like\\this.txt to c:/names/like/this.txt"""
    for i,fname in enumerate(listOfFiles):
        listOfFiles[i]=fname.replace("\\","/")
    return listOfFiles