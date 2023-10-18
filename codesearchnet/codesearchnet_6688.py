def economic_status(self):
        r'''Dictionary of economic status indicators for the chemical.

        Examples
        --------
        >>> pprint(Chemical('benzene').economic_status)
        ["US public: {'Manufactured': 6165232.1, 'Imported': 463146.474, 'Exported': 271908.252}",
         u'1,000,000 - 10,000,000 tonnes per annum',
         u'Intermediate Use Only',
         'OECD HPV Chemicals']
        '''
        if self.__economic_status:
            return self.__economic_status
        else:
            self.__economic_status = economic_status(self.CAS, Method='Combined')
            return self.__economic_status