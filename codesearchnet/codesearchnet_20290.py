def compute_sha256(filename):
    """
    Try the library. If it doesnt work, use the command line..
    """
    try:
        h = sha256()
        fd = open(filename, 'rb')
        while True:
            buf = fd.read(0x1000000)
            if buf in [None, ""]:
                break
            h.update(buf.encode('utf-8'))
        fd.close()
        return h.hexdigest()
    except:
        output = run(["sha256sum", "-b", filename])
        return output.split(" ")[0]