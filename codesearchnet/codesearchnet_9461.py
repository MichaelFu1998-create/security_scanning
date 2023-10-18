def stor(ftp=None):
    """Same as ftplib's storbinary() but just sends dummy data
    instead of reading it from a real file.
    """
    if ftp is None:
        ftp = connect()
        quit = True
    else:
        quit = False
    ftp.voidcmd('TYPE I')
    with contextlib.closing(ftp.transfercmd("STOR " + TESTFN)) as conn:
        chunk = b'x' * BUFFER_LEN
        total_sent = 0
        while True:
            sent = conn.send(chunk)
            total_sent += sent
            if total_sent >= FILE_SIZE:
                break
    ftp.voidresp()
    if quit:
        ftp.quit()
    return ftp