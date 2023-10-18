async def download(self, source, destination="", *, write_into=False,
                       block_size=DEFAULT_BLOCK_SIZE):
        """
        :py:func:`asyncio.coroutine`

        High level download method for downloading files and directories
        recursively and save them to the file system.

        :param source: source path of file or directory on server side
        :type source: :py:class:`str` or :py:class:`pathlib.PurePosixPath`

        :param destination: destination path of file or directory on client
            side
        :type destination: :py:class:`str` or :py:class:`pathlib.Path`

        :param write_into: write source into destination (if you want download
            file and change it name, as well with directories)
        :type write_into: :py:class:`bool`

        :param block_size: block size for transaction
        :type block_size: :py:class:`int`
        """
        source = pathlib.PurePosixPath(source)
        destination = pathlib.Path(destination)
        if not write_into:
            destination = destination / source.name
        if await self.is_file(source):
            await self.path_io.mkdir(destination.parent,
                                     parents=True, exist_ok=True)
            async with self.path_io.open(destination, mode="wb") as file_out, \
                    self.download_stream(source) as stream:
                async for block in stream.iter_by_block(block_size):
                    await file_out.write(block)
        elif await self.is_dir(source):
            await self.path_io.mkdir(destination, parents=True, exist_ok=True)
            for name, info in (await self.list(source)):
                full = destination / name.relative_to(source)
                if info["type"] in ("file", "dir"):
                    await self.download(name, full, write_into=True,
                                        block_size=block_size)