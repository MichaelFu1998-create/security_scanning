def set_shared_config(cls, config):
        """ This allows to set a config that will be used when calling
            ``shared_blockchain_instance`` and allows to define the configuration
            without requiring to actually create an instance
        """
        assert isinstance(config, dict)
        cls._sharedInstance.config.update(config)
        # if one is already set, delete
        if cls._sharedInstance.instance:
            cls._sharedInstance.instance = None