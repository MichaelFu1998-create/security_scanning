def finalize(self):
        """
        finalize partial fitting procedure
        """
        if self.__head_less:
            warn(f'{self.__class__.__name__} configured to head less mode. finalize unusable')
        elif not self.__head_generate:
            warn(f'{self.__class__.__name__} already finalized or fitted')
        elif not self.__head_dict:
            raise NotFittedError(f'{self.__class__.__name__} instance is not fitted yet')
        else:
            if self.remove_rare_ratio:
                self.__clean_head(*self.__head_rare)
                self.__prepare_header()
                self.__head_rare = None
            self.__head_generate = False