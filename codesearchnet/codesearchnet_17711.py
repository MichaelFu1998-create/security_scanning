def get_vacations():
        """
        Pull the accounts vacations.
        """
        arequest = requests.get(VACATIONS_URL, headers=HEADERS)
        status_code = str(arequest.status_code)
        if status_code == '401':
            _LOGGER.error("Token expired.")
            return False
        return arequest.json()