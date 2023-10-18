def _process_event(self, key, mask):
        """Selector has delivered us an event."""
        self._logger.debug('Processing event with key {} and mask {}'.format(key, mask))
        fileobj, (reader, writer) = key.fileobj, key.data
        if mask & selectors.EVENT_READ and reader is not None:
            if reader._cancelled:
                self.remove_reader(fileobj)
            else:
                self._logger.debug('Invoking reader callback: {}'.format(reader))
                reader._run()
        if mask & selectors.EVENT_WRITE and writer is not None:
            if writer._cancelled:
                self.remove_writer(fileobj)
            else:
                self._logger.debug('Invoking writer callback: {}'.format(writer))
                writer._run()