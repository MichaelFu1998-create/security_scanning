def get_device(_id):
        """
        Pull a device from the API.
        """
        url = DEVICE_URL % _id
        arequest = requests.get(url, headers=HEADERS)
        status_code = str(arequest.status_code)
        if status_code == '401':
            _LOGGER.error("Token expired.")
            return False
        return arequest.json()