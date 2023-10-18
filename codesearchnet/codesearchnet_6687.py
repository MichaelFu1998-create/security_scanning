def legal_status(self):
        r'''Dictionary of legal status indicators for the chemical.

        Examples
        --------
        >>> pprint(Chemical('benzene').legal_status)
        {'DSL': 'LISTED',
         'EINECS': 'LISTED',
         'NLP': 'UNLISTED',
         'SPIN': 'LISTED',
         'TSCA': 'LISTED'}
        '''
        if self.__legal_status:
            return self.__legal_status
        else:
            self.__legal_status = legal_status(self.CAS, Method='COMBINED')
            return self.__legal_status