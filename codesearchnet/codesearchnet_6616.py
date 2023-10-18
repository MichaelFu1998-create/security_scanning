def _reset(self):
        """
        Initializes the :class:`Harvester` object. Once you reset the
        :class:`Harvester` object, all allocated resources, including buffers
        and remote device, will be released.

        :return: None.
        """
        #
        for ia in self._ias:
            ia._destroy()

        self._ias.clear()

        #
        self._logger.info('Started resetting the Harvester object.')
        self.remove_cti_files()
        self._release_gentl_producers()

        if self._profiler:
            self._profiler.print_diff()

        #
        self._logger.info('Completed resetting the Harvester object.')