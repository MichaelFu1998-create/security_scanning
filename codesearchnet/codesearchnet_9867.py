def tabular(self):
        """https://github.com/frictionlessdata/datapackage-py#resource
        """
        if self.__current_descriptor.get('profile') == 'tabular-data-resource':
            return True
        if not self.__strict:
            if self.__current_descriptor.get('format') in config.TABULAR_FORMATS:
                return True
            if self.__source_inspection.get('tabular', False):
                return True
        return False