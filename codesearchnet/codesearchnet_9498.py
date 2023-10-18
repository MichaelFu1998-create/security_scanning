async def stat(self, path):
        """
        :py:func:`asyncio.coroutine`

        Getting path stats.

        :param path: path for getting info
        :type path: :py:class:`str` or :py:class:`pathlib.PurePosixPath`

        :return: path info
        :rtype: :py:class:`dict`
        """
        path = pathlib.PurePosixPath(path)
        try:
            code, info = await self.command("MLST " + str(path), "2xx")
            name, info = self.parse_mlsx_line(info[1].lstrip())
            return info
        except errors.StatusCodeError as e:
            if not e.received_codes[-1].matches("50x"):
                raise

        for p, info in await self.list(path.parent):
            if p.name == path.name:
                return info
        else:
            raise errors.StatusCodeError(
                Code("2xx"),
                Code("550"),
                "path does not exists",
            )