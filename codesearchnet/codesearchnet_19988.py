def pprint_args(self, pos_args, keyword_args, infix_operator=None, extra_params={}):
        """
        Method to define the positional arguments and keyword order
        for pretty printing.
        """
        if infix_operator and not (len(pos_args)==2 and keyword_args==[]):
            raise Exception('Infix format requires exactly two'
                            ' positional arguments and no keywords')
        (kwargs,_,_,_) = self._pprint_args
        self._pprint_args = (keyword_args + kwargs, pos_args, infix_operator, extra_params)