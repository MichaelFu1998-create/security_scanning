def _configuration(self, kwargs, config_item):
        """Combine configuration-related keyworded arguments into
        notification_configuration.
        """
        if 'notification_configuration' not in config_item:
            if 'notification_type' not in kwargs:
                return
            nc = kwargs['notification_configuration'] = {}
            for field in Resource.configuration[kwargs['notification_type']]:
                if field not in config_item:
                    raise exc.TowerCLIError('Required config field %s not'
                                            ' provided.' % field)
                else:
                    nc[field] = config_item[field]
        else:
            kwargs['notification_configuration'] = \
                    config_item['notification_configuration']