def set_state(_id, body):
        """
        Set a devices state.
        """
        url = DEVICE_URL % _id
        if "mode" in body:
            url = MODES_URL % _id
        arequest = requests.put(url, headers=HEADERS, data=json.dumps(body))
        status_code = str(arequest.status_code)
        if status_code != '202':
            _LOGGER.error("State not accepted. " + status_code)
            return False