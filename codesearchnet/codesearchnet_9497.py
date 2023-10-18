def list(self, path="", *, recursive=False, raw_command=None):
        """
        :py:func:`asyncio.coroutine`

        List all files and directories in "path".

        :param path: directory or file path
        :type path: :py:class:`str` or :py:class:`pathlib.PurePosixPath`

        :param recursive: list recursively
        :type recursive: :py:class:`bool`

        :param raw_command: optional ftp command to use in place of
            fallback logic (must be one of "MLSD", "LIST")
        :type raw_command: :py:class:`str`

        :rtype: :py:class:`list` or `async for` context

        ::

            >>> # lazy list
            >>> async for path, info in client.list():
            ...     # no interaction with client should be here(!)

            >>> # eager list
            >>> for path, info in (await client.list()):
            ...     # interaction with client allowed, since all paths are
            ...     # collected already

        ::

            >>> stats = await client.list()
        """
        class AsyncLister(AsyncListerMixin):
            stream = None

            async def _new_stream(cls, local_path):
                cls.path = local_path
                cls.parse_line = self.parse_mlsx_line
                if raw_command not in [None, "MLSD", "LIST"]:
                    raise ValueError("raw_command must be one of MLSD or "
                                     f"LIST, but got {raw_command}")
                if raw_command in [None, "MLSD"]:
                    try:
                        command = ("MLSD " + str(cls.path)).strip()
                        return await self.get_stream(command, "1xx")
                    except errors.StatusCodeError as e:
                        code = e.received_codes[-1]
                        if not code.matches("50x") or raw_command is not None:
                            raise
                if raw_command in [None, "LIST"]:
                    cls.parse_line = self.parse_list_line
                    command = ("LIST " + str(cls.path)).strip()
                    return await self.get_stream(command, "1xx")

            def __aiter__(cls):
                cls.directories = collections.deque()
                return cls

            async def __anext__(cls):
                if cls.stream is None:
                    cls.stream = await cls._new_stream(path)
                while True:
                    line = await cls.stream.readline()
                    while not line:
                        await cls.stream.finish()
                        if cls.directories:
                            current_path, info = cls.directories.popleft()
                            cls.stream = await cls._new_stream(current_path)
                            line = await cls.stream.readline()
                        else:
                            raise StopAsyncIteration

                    try:
                        name, info = cls.parse_line(line)
                    except Exception:
                        continue

                    stat = cls.path / name, info
                    if info["type"] == "dir" and recursive:
                        cls.directories.append(stat)
                    return stat

        return AsyncLister()