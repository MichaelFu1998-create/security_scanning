def get_modes(_id):
        """
        Pull a water heater's modes from the API.
        """
        url = MODES_URL % _id
        arequest = requests.get(url, headers=HEADERS)
        status_code = str(arequest.status_code)
        if status_code == '401':
            _LOGGER.error("Token expired.")
            return False
        return arequest.json()