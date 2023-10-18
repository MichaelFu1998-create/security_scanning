def parse_translations(self, markup):
        
        """ Returns a dictionary of translations for the page title.
        
        A Wikipedia language link looks like: [[af:Rekenaar]].
        The parser will also fetch links like "user:" and "media:"
        but these are stripped against the dictionary of
        Wikipedia languages.
        
        You can get a translated page by searching Wikipedia
        with the appropriate language code and supplying
        the translated title as query.
        
        """
        
        global languages
        translations = {}
        m = re.findall(self.re["translation"], markup)
        for language, translation in m:
            if language in languages:
                translations[language] = translation
         
        return translations