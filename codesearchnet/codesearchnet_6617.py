def update_device_info_list(self):
        """
        Updates the device information list. You'll have to call this method
        every time you added CTI files or plugged/unplugged devices.

        :return: None.
        """
        #
        self._release_gentl_producers()

        try:
            self._open_gentl_producers()
            self._open_systems()
            #
            for system in self._systems:
                #
                system.update_interface_info_list(self.timeout_for_update)

                #
                for i_info in system.interface_info_list:
                    iface = i_info.create_interface()
                    try:
                        iface.open()
                    except (
                        NotInitializedException, ResourceInUseException,
                        InvalidHandleException, InvalidHandleException,
                        InvalidParameterException, AccessDeniedException,
                    ) as e:
                        self._logger.debug(e, exc_info=True)
                    else:
                        self._logger.info(
                            'Opened Interface module, {0}.'.format(iface.id_)
                        )
                        iface.update_device_info_list(self.timeout_for_update)
                        self._interfaces.append(iface)
                        for d_info in iface.device_info_list:
                            self.device_info_list.append(d_info)

        except LoadLibraryException as e:
            self._logger.error(e, exc_info=True)
            self._has_revised_device_list = False
        else:
            self._has_revised_device_list = True

        #
        self._logger.info('Updated the device information list.')