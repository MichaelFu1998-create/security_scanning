def retr(ftp):
    """Same as ftplib's retrbinary() but discard the received data."""
    ftp.voidcmd('TYPE I')
    with contextlib.closing(ftp.transfercmd("RETR " + TESTFN)) as conn:
        recv_bytes = 0
        while True:
            data = conn.recv(BUFFER_LEN)
            if not data:
                break
            recv_bytes += len(data)
    ftp.voidresp()