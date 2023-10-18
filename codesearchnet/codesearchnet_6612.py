def fetch_buffer(self, *, timeout=0, is_raw=False):
        """
        Fetches the latest :class:`Buffer` object and returns it.

        :param timeout: Set timeout value in second.
        :param is_raw: Set :const:`True` if you need a raw GenTL Buffer module.

        :return: A :class:`Buffer` object.
        """
        if not self.is_acquiring_images:
            raise TimeoutException

        watch_timeout = True if timeout > 0 else False
        buffer = None
        base = time.time()

        while buffer is None:
            if watch_timeout and (time.time() - base) > timeout:
                raise TimeoutException
            else:
                with MutexLocker(self.thread_image_acquisition):
                    if len(self._holding_filled_buffers) > 0:
                        if is_raw:
                            buffer = self._holding_filled_buffers.pop(0)
                        else:
                            # Update the chunk data:
                            _buffer = self._holding_filled_buffers.pop(0)
                            self._update_chunk_data(buffer=_buffer)
                            #
                            buffer = Buffer(
                                buffer=_buffer,
                                node_map=self.device.node_map,
                                logger=self._logger
                            )

        if _is_logging_buffer_manipulation:
            self._logger.debug(
                'Fetched Buffer module #{0}'
                ' containing frame #{1}'
                ' of DataStream module {2}'
                ' of Device module {2}'
                '.'.format(
                    buffer._buffer.context,
                    buffer._buffer.frame_id,
                    buffer._buffer.parent.id_,
                    buffer._buffer.parent.parent.id_
                )
            )

        return buffer