def delete_vacation(_id):
        """
        Delete a vacation by ID.
        """
        arequest = requests.delete(VACATIONS_URL + "/" + _id, headers=HEADERS)
        status_code = str(arequest.status_code)
        if status_code != '202':
            _LOGGER.error("Failed to delete vacation. " + status_code)
            return False
        return True