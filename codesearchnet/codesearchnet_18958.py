def get_stepper_version(self, timeout=20):
        """
        Get the stepper library version number.

        :param timeout: specify a time to allow arduino to process and return a version

        :return: the stepper version number if it was set.
        """
        # get current time
        start_time = time.time()

        # wait for up to 20 seconds for a successful capability query to occur

        while self._command_handler.stepper_library_version <= 0:
            if time.time() - start_time > timeout:
                if self.verbose is True:
                    print("Stepper Library Version Request timed-out. "
                          "Did you send a stepper_request_library_version command?")
                return
            else:
                pass
        return self._command_handler.stepper_library_version