def _wait_for_connection(self, port):
        """
        Wait until we can make a socket connection to sphinx.
        """
        connected = False
        max_tries = 10
        num_tries = 0
        wait_time = 0.5
        while not connected or num_tries >= max_tries:
            time.sleep(wait_time)
            try:
                af = socket.AF_INET
                addr = ('127.0.0.1', port)
                sock = socket.socket(af, socket.SOCK_STREAM)
                sock.connect(addr)
            except socket.error:
                if sock:
                    sock.close()
                num_tries += 1
                continue
            connected = True

        if not connected:
            print("Error connecting to sphinx searchd", file=sys.stderr)