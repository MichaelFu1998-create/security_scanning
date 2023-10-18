def start_image_acquisition(self):
        """
        Starts image acquisition.

        :return: None.
        """
        if not self._create_ds_at_connection:
            self._setup_data_streams()

        #
        num_required_buffers = self._num_buffers
        for data_stream in self._data_streams:
            try:
                num_buffers = data_stream.buffer_announce_min
                if num_buffers < num_required_buffers:
                    num_buffers = num_required_buffers
            except InvalidParameterException as e:
                num_buffers = num_required_buffers
                self._logger.debug(e, exc_info=True)

            if data_stream.defines_payload_size():
                buffer_size = data_stream.payload_size
            else:
                buffer_size = self.device.node_map.PayloadSize.value

            raw_buffers = self._create_raw_buffers(
                num_buffers, buffer_size
            )

            buffer_tokens = self._create_buffer_tokens(
                raw_buffers
            )

            self._announced_buffers = self._announce_buffers(
                data_stream=data_stream, _buffer_tokens=buffer_tokens
            )

            self._queue_announced_buffers(
                data_stream=data_stream, buffers=self._announced_buffers
            )

        # Reset the number of images to acquire.
        try:
            acq_mode = self.device.node_map.AcquisitionMode.value
            if acq_mode == 'Continuous':
                num_images_to_acquire = -1
            elif acq_mode == 'SingleFrame':
                num_images_to_acquire = 1
            elif acq_mode == 'MultiFrame':
                num_images_to_acquire = self.device.node_map.AcquisitionFrameCount.value
            else:
                num_images_to_acquire = -1
        except LogicalErrorException as e:
            # The node doesn't exist.
            num_images_to_acquire = -1
            self._logger.debug(e, exc_info=True)

        self._num_images_to_acquire = num_images_to_acquire

        try:
            # We're ready to start image acquisition. Lock the device's
            # transport layer related features:
            self.device.node_map.TLParamsLocked.value = 1
        except LogicalErrorException:
            # SFNC < 2.0
            pass

        # Start image acquisition.
        self._is_acquiring_images = True

        for data_stream in self._data_streams:
            data_stream.start_acquisition(
                ACQ_START_FLAGS_LIST.ACQ_START_FLAGS_DEFAULT,
                self._num_images_to_acquire
            )

        #
        if self.thread_image_acquisition:
            self.thread_image_acquisition.start()

        #
        self.device.node_map.AcquisitionStart.execute()

        self._logger.info(
            '{0} started image acquisition.'.format(self._device.id_)
        )

        if self._profiler:
            self._profiler.print_diff()