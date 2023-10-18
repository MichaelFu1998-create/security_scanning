async def write_response(self, stream, code, lines="", list=False):
        """
        :py:func:`asyncio.coroutine`

        Complex method for sending response.

        :param stream: command connection stream
        :type stream: :py:class:`aioftp.StreamIO`

        :param code: server response code
        :type code: :py:class:`str`

        :param lines: line or lines, which are response information
        :type lines: :py:class:`str` or :py:class:`collections.Iterable`

        :param list: if true, then lines will be sended without code prefix.
            This is useful for **LIST** FTP command and some others.
        :type list: :py:class:`bool`
        """
        lines = wrap_with_container(lines)
        write = functools.partial(self.write_line, stream)
        if list:
            head, *body, tail = lines
            await write(code + "-" + head)
            for line in body:
                await write(" " + line)
            await write(code + " " + tail)
        else:
            *body, tail = lines
            for line in body:
                await write(code + "-" + line)
            await write(code + " " + tail)