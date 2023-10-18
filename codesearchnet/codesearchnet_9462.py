def bytes_per_second(ftp, retr=True):
    """Return the number of bytes transmitted in 1 second."""
    tot_bytes = 0
    if retr:
        def request_file():
            ftp.voidcmd('TYPE I')
            conn = ftp.transfercmd("retr " + TESTFN)
            return conn

        with contextlib.closing(request_file()) as conn:
            register_memory()
            stop_at = time.time() + 1.0
            while stop_at > time.time():
                chunk = conn.recv(BUFFER_LEN)
                if not chunk:
                    a = time.time()
                    ftp.voidresp()
                    conn.close()
                    conn = request_file()
                    stop_at += time.time() - a
                tot_bytes += len(chunk)

        try:
            while chunk:
                chunk = conn.recv(BUFFER_LEN)
            ftp.voidresp()
            conn.close()
        except (ftplib.error_temp, ftplib.error_perm):
            pass
    else:
        ftp.voidcmd('TYPE I')
        with contextlib.closing(ftp.transfercmd("STOR " + TESTFN)) as conn:
            register_memory()
            chunk = b'x' * BUFFER_LEN
            stop_at = time.time() + 1
            while stop_at > time.time():
                tot_bytes += conn.send(chunk)
        ftp.voidresp()

    return tot_bytes