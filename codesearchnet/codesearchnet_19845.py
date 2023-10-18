def determineProtocol(fname):
    """determine the comment cooked in the protocol."""
    f=open(fname,'rb')
    raw=f.read(5000) #it should be in the first 5k of the file
    f.close()
    protoComment="unknown"
    if b"SWHLab4[" in raw:
        protoComment=raw.split(b"SWHLab4[")[1].split(b"]",1)[0]
    elif b"SWH[" in raw:
        protoComment=raw.split(b"SWH[")[1].split(b"]",1)[0]
    else:
        protoComment="?"
    if not type(protoComment) is str:
        protoComment=protoComment.decode("utf-8")
    return protoComment