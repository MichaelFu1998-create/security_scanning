def send_command(self, cmd, *args):
        """
        :param cmd:
        :param args:
        :return:
        """
        # Test in python 2 and 3 before modifying (gedit2 + 3)
        if True:
            # Create a CommandResponse using a cookie as a unique id
            cookie = str(uuid.uuid4())
            response = CommandResponse(cmd, cookie, None, info=[])
            self.responses[cookie] = response
            args = list(args) + [b'cookie=' + bytes(cookie, "ascii")]
        if args:
            bytes_args = []
            for arg in args:
                if isinstance(arg, bytes):
                    bytes_args.append(arg)
                else:
                    bytes_args.append(bytearray(arg, "ascii"))
            data = bytearray(cmd, "ascii") + b' ' + b' '.join(bytes_args) + b'\n'
        else:
            data = bytearray(cmd, "ascii") + b'\n'

        self.process.stdin.write(data)
        self.process.stdin.flush()