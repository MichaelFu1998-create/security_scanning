def create_vacation(body):
        """
        Create a vacation.
        """
        arequest = requests.post(VACATIONS_URL, headers=HEADERS, data=json.dumps(body))
        status_code = str(arequest.status_code)
        if status_code != '200':
            _LOGGER.error("Failed to create vacation. " + status_code)
            _LOGGER.error(arequest.json())
            return False
        return arequest.json()