def _destroy_image_acquirer(self, ia):
        """
        Releases all external resources including the controlling device.
        """

        id_ = None
        if ia.device:
            #
            ia.stop_image_acquisition()

            #
            ia._release_data_streams()

            #
            id_ = ia._device.id_

            #
            if ia.device.node_map:
                #
                if ia._chunk_adapter:
                    ia._chunk_adapter.detach_buffer()
                    ia._chunk_adapter = None
                    self._logger.info(
                        'Detached a buffer from the chunk adapter of {0}.'.format(
                            id_
                        )
                    )

                ia.device.node_map.disconnect()
                self._logger.info(
                    'Disconnected the port from the NodeMap of {0}.'.format(
                        id_
                    )
                )

            #
            if ia._device.is_open():
                ia._device.close()
                self._logger.info(
                    'Closed Device module, {0}.'.format(id_)
                )

        ia._device = None

        #
        if id_:
            self._logger.info(
                'Destroyed the ImageAcquirer object which {0} '
                'had belonged to.'.format(id_)
            )
        else:
            self._logger.info(
                'Destroyed an ImageAcquirer.'
            )

        if self._profiler:
            self._profiler.print_diff()

        self._ias.remove(ia)