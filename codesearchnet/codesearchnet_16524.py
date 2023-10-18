def __refill_tokenbuffer(self):
        """Add a new tokenized line from the file to the token buffer.

        __refill_tokenbuffer()

        Only reads a new line if the buffer is empty. It is safe to
        call it repeatedly.

        At end of file, method returns empty strings and it is up to
        __peek and __consume to flag the end of the stream.
        """
        if len(self.tokens) == 0:
            self.__tokenize(self.dxfile.readline())