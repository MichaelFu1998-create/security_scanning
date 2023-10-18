def _reset(self):
        """Reset internal data-dependent state.
        __init__ parameters are not touched.
        """
        if not self.__head_less:
            if not self.__head_generate:
                self.__head_generate = True
            if self.__head_dict:
                self.__head_dump = self.__head_dict = None
            if self.__head_rare is not None:
                self.__head_rare = None

            self.delete_work_path()