def reset(self):
        """Reset repository instance.
        """
        self.__path   = None
        self.__repo   = {'repository_unique_name': str(uuid.uuid1()),
                         'create_utctime': time.time(),
                         'last_update_utctime': None,
                         'pyrep_version': str(__version__),
                         'repository_information': '',
                         'walk_repo': []}