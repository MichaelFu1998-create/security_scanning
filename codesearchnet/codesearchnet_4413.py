def construct_start_message(self):
        """Collect preliminary run info at the start of the DFK.

        Returns :
              - Message dict dumped as json string, ready for UDP
        """
        uname = getpass.getuser().encode('latin1')
        hashed_username = hashlib.sha256(uname).hexdigest()[0:10]
        hname = socket.gethostname().encode('latin1')
        hashed_hostname = hashlib.sha256(hname).hexdigest()[0:10]
        message = {'uuid': self.uuid,
                   'uname': hashed_username,
                   'hname': hashed_hostname,
                   'test': self.test_mode,
                   'parsl_v': self.parsl_version,
                   'python_v': self.python_version,
                   'os': platform.system(),
                   'os_v': platform.release(),
                   'start': time.time()}

        return json.dumps(message)