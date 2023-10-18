def _send_login(self):
        """
        Sends login string to server
        """
        login_str = "user {0} pass {1} vers aprslib {3}{2}\r\n"
        login_str = login_str.format(
            self.callsign,
            self.passwd,
            (" filter " + self.filter) if self.filter != "" else "",
            __version__
            )

        self.logger.info("Sending login information")

        try:
            self._sendall(login_str)
            self.sock.settimeout(5)
            test = self.sock.recv(len(login_str) + 100)
            if is_py3:
                test = test.decode('latin-1')
            test = test.rstrip()

            self.logger.debug("Server: %s", test)

            _, _, callsign, status, _ = test.split(' ', 4)

            if callsign == "":
                raise LoginError("Server responded with empty callsign???")
            if callsign != self.callsign:
                raise LoginError("Server: %s" % test)
            if status != "verified," and self.passwd != "-1":
                raise LoginError("Password is incorrect")

            if self.passwd == "-1":
                self.logger.info("Login successful (receive only)")
            else:
                self.logger.info("Login successful")

        except LoginError as e:
            self.logger.error(str(e))
            self.close()
            raise
        except:
            self.close()
            self.logger.error("Failed to login")
            raise LoginError("Failed to login")