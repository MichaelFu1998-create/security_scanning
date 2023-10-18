def startProducing(self, consumer):
        """ Start producing.

        Args:
            consumer: Consumer
        """
        self._consumer = consumer
        self._current_deferred = defer.Deferred()
        self._sent = 0
        self._paused = False

        if not hasattr(self, "_chunk_headers"):
            self._build_chunk_headers()

        if self._data:
            block = ""
            for field in self._data:
                block += self._chunk_headers[field]
                block += self._data[field]
                block += "\r\n"

            self._send_to_consumer(block)

        if self._files:
            self._files_iterator = self._files.iterkeys()
            self._files_sent = 0
            self._files_length = len(self._files)
            self._current_file_path = None
            self._current_file_handle = None
            self._current_file_length = None
            self._current_file_sent = 0

            result = self._produce()
            if result:
                return result
        else:
            return defer.succeed(None)

        return self._current_deferred