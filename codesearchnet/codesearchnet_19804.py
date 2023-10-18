def abfProtocol(fname):
    """Determine the protocol used to record an ABF file"""
    f=open(fname,'rb')
    raw=f.read(30*1000) #it should be in the first 30k of the file
    f.close()
    raw=raw.decode("utf-8","ignore")
    raw=raw.split("Clampex")[1].split(".pro")[0]
    protocol = os.path.basename(raw) # the whole protocol filename
    protocolID = protocol.split(" ")[0] # just the first number
    return protocolID