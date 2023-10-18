def get_usage(_id):
        """
        Pull a water heater's usage report from the API.
        """
        url = USAGE_URL % _id
        arequest = requests.get(url, headers=HEADERS)
        status_code = str(arequest.status_code)
        if status_code == '401':
            _LOGGER.error("Token expired.")
            return False
        try:
            return arequest.json()
        except ValueError:
            _LOGGER.info("Failed to get usage. Not supported by unit?")
            return None