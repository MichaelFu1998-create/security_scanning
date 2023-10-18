def get_data(self):
        """Get current light data as dictionary with light zids as keys."""
        response = self.send_command(GET_LIGHTS_COMMAND)
        _LOGGER.debug("get_data response: %s", repr(response))
        if not response:
            _LOGGER.debug("Empty response: %s", response)
            return {}
        response = response.strip()
        # Check string before splitting (avoid IndexError if malformed)
        if not (response.startswith("GLB") and response.endswith(";")):
            _LOGGER.debug("Invalid response: %s", repr(response))
            return {}

        # deconstruct response string into light data. Example data:
        # GLB 143E,1,1,25,255,255,255,0,0;287B,1,1,22,255,255,255,0,0;\r\n
        response = response[4:-3]  # strip start (GLB) and end (;\r\n)
        light_strings = response.split(';')
        light_data_by_id = {}
        for light_string in light_strings:
            values = light_string.split(',')
            try:
                light_data_by_id[values[0]] = [int(values[2]), int(values[4]),
                                               int(values[5]), int(values[6]),
                                               int(values[7])]
            except ValueError as error:
                _LOGGER.error("Error %s: %s (%s)", error, values, response)
            except IndexError as error:
                _LOGGER.error("Error %s: %s (%s)", error, values, response)
        return light_data_by_id