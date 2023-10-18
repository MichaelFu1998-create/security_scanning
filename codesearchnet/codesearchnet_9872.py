def commit(self, strict=None):
        """https://github.com/frictionlessdata/datapackage-py#resource
        """
        if strict is not None:
            self.__strict = strict
        elif self.__current_descriptor == self.__next_descriptor:
            return False
        self.__current_descriptor = deepcopy(self.__next_descriptor)
        self.__table = None
        self.__build()
        return True