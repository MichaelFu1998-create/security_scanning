def generate_api(version):
    """
    Generates a factory function to instantiate the API with the given
    version.

    """
    def get_partial_api(key, token=None):
        return TrelloAPI(ENDPOINTS[version], version, key, token=token)

    get_partial_api.__doc__ = \
        """Interfaz REST con Trello. Versión {}""".format(version)

    return get_partial_api