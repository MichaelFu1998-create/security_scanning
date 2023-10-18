def stop_image_acquisition(self):
        """
        Stops image acquisition.

        :return: None.
        """
        if self.is_acquiring_images:
            #
            self._is_acquiring_images = False

            #
            if self.thread_image_acquisition.is_running:  # TODO
                self.thread_image_acquisition.stop()

            with MutexLocker(self.thread_image_acquisition):
                #
                self.device.node_map.AcquisitionStop.execute()

                try:
                    # Unlock TLParamsLocked in order to allow full device
                    # configuration:
                    self.device.node_map.TLParamsLocked.value = 0
                except LogicalErrorException:
                    # SFNC < 2.0
                    pass

                for data_stream in self._data_streams:
                    # Stop image acquisition.
                    try:
                        data_stream.stop_acquisition(
                            ACQ_STOP_FLAGS_LIST.ACQ_STOP_FLAGS_KILL
                        )
                    except (ResourceInUseException, TimeoutException) as e:
                        self._logger.error(e, exc_info=True)

                    # Flash the queue for image acquisition process.
                    data_stream.flush_buffer_queue(
                        ACQ_QUEUE_TYPE_LIST.ACQ_QUEUE_ALL_DISCARD
                    )

                for event_manager in self._event_new_buffer_managers:
                    event_manager.flush_event_queue()

                if self._create_ds_at_connection:
                    self._release_buffers()
                else:
                    self._release_data_streams()

            #
            self._has_acquired_1st_image = False

            #
            self._chunk_adapter.detach_buffer()

            #
            self._logger.info(
                '{0} stopped image acquisition.'.format(self._device.id_)
            )

        if self._profiler:
            self._profiler.print_diff()