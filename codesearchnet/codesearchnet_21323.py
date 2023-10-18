def get_locale(self):
        """ Retrieve the best matching locale using request headers

        .. note:: Probably one of the thing to enhance quickly.

        :rtype: str
        """
        best_match = request.accept_languages.best_match(['de', 'fr', 'en', 'la'])
        if best_match is None:
            if len(request.accept_languages) > 0:
                best_match = request.accept_languages[0][0][:2]
            else:
                return self.__default_lang__
        lang = self.__default_lang__
        if best_match == "de":
            lang = "ger"
        elif best_match == "fr":
            lang = "fre"
        elif best_match == "en":
            lang = "eng"
        elif best_match == "la":
            lang = "lat"
        return lang