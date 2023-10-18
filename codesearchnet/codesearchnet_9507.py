async def get_passive_connection(self, conn_type="I",
                                     commands=("epsv", "pasv")):
        """
        :py:func:`asyncio.coroutine`

        Getting pair of reader, writer for passive connection with server.

        :param conn_type: connection type ("I", "A", "E", "L")
        :type conn_type: :py:class:`str`

        :param commands: sequence of commands to try to initiate passive
            server creation. First success wins. Default is EPSV, then PASV.
        :type commands: :py:class:`list`

        :rtype: (:py:class:`asyncio.StreamReader`,
            :py:class:`asyncio.StreamWriter`)
        """
        functions = {
            "epsv": self._do_epsv,
            "pasv": self._do_pasv,
        }
        if not commands:
            raise ValueError("No passive commands provided")
        await self.command("TYPE " + conn_type, "200")
        for i, name in enumerate(commands, start=1):
            name = name.lower()
            if name not in functions:
                raise ValueError(f"{name!r} not in {set(functions)!r}")
            try:
                ip, port = await functions[name]()
                break
            except errors.StatusCodeError as e:
                is_last = i == len(commands)
                if is_last or not e.received_codes[-1].matches("50x"):
                    raise
        if ip in ("0.0.0.0", None):
            ip = self.server_host
        reader, writer = await open_connection(
            ip,
            port,
            self.create_connection,
            self.ssl,
        )
        return reader, writer