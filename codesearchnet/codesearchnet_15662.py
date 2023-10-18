def consumer(self, callback, blocking=True, immortal=False, raw=False):
        """
        When a position sentence is received, it will be passed to the callback function

        blocking: if true (default), runs forever, otherwise will return after one sentence
                  You can still exit the loop, by raising StopIteration in the callback function

        immortal: When true, consumer will try to reconnect and stop propagation of Parse exceptions
                  if false (default), consumer will return

        raw: when true, raw packet is passed to callback, otherwise the result from aprs.parse()
        """

        if not self._connected:
            raise ConnectionError("not connected to a server")

        line = b''

        while True:
            try:
                for line in self._socket_readlines(blocking):
                    if line[0:1] != b'#':
                        if raw:
                            callback(line)
                        else:
                            callback(self._parse(line))
                    else:
                        self.logger.debug("Server: %s", line.decode('utf8'))
            except ParseError as exp:
                self.logger.log(11, "%s\n    Packet: %s", exp.message, exp.packet)
            except UnknownFormat as exp:
                self.logger.log(9, "%s\n    Packet: %s", exp.message, exp.packet)
            except LoginError as exp:
                self.logger.error("%s: %s", exp.__class__.__name__, exp.message)
            except (KeyboardInterrupt, SystemExit):
                raise
            except (ConnectionDrop, ConnectionError):
                self.close()

                if not immortal:
                    raise
                else:
                    self.connect(blocking=blocking)
                    continue
            except GenericError:
                pass
            except StopIteration:
                break
            except:
                self.logger.error("APRS Packet: %s", line)
                raise

            if not blocking:
                break