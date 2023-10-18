def send_command(
        self, command, callback=True, command_type=QRTPacketType.PacketCommand
    ):
        """ Sends commands to QTM """
        if self.transport is not None:
            cmd_length = len(command)
            LOG.debug("S: %s", command)
            self.transport.write(
                struct.pack(
                    RTCommand % cmd_length,
                    RTheader.size + cmd_length + 1,
                    command_type.value,
                    command.encode(),
                    b"\0",
                )
            )

            future = self.loop.create_future()
            if callback:
                self.request_queue.append(future)
            else:
                future.set_result(None)
            return future

        raise QRTCommandException("Not connected!")