def get_locations():
        """
        Pull the accounts locations.
        """
        arequest = requests.get(LOCATIONS_URL, headers=HEADERS)
        status_code = str(arequest.status_code)
        if status_code == '401':
            _LOGGER.error("Token expired.")
            return False
        return arequest.json()