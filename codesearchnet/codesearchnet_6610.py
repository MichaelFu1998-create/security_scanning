def queue(self):
        """
        Queues the buffer to prepare for the upcoming image acquisition. Once
        the buffer is queued, the :class:`Buffer` object will be obsolete.
        You'll have nothing to do with it.

        Note that you have to return the ownership of the fetched buffers to
        the :class:`ImageAcquirer` object before stopping image acquisition
        calling this method because the :class:`ImageAcquirer` object tries
        to clear the self-allocated buffers when it stops image acquisition.
        """
        #
        if _is_logging_buffer_manipulation:
            self._logger.debug(
                'Queued Buffer module #{0}'
                ' containing frame #{1}'
                ' to DataStream module {2}'
                ' of Device module {3}'
                '.'.format(
                    self._buffer.context,
                    self._buffer.frame_id,
                    self._buffer.parent.id_,
                    self._buffer.parent.parent.id_
                )
            )

        self._buffer.parent.queue_buffer(self._buffer)