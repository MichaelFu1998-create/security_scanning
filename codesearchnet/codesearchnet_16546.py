def get_devices(self):
        """
        Get all devices

        :return:
            A list of AmbientWeatherStation instances.
        """
        retn = []
        api_devices = self.api_call('devices')

        self.log('DEVICES:')
        self.log(api_devices)

        for device in api_devices:
            retn.append(AmbientWeatherStation(self, device))

        self.log('DEVICE INSTANCE LIST:')
        self.log(retn)

        return retn