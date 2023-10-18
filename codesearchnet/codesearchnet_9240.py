def set_param(self, section, param, value):
        """ Change a param in the config """
        if section not in self.conf or param not in self.conf[section]:
            logger.error('Config section %s and param %s not exists', section, param)
        else:
            self.conf[section][param] = value