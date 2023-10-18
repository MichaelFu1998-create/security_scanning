def verifysettext(self, window_name, object_name, text):
        """
        Verify text is set correctly
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param text: text to match
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        try:
            return int(re.match(fnmatch.translate(text),
                                self.gettextvalue(window_name,
                                                  object_name)))
        except:
            return 0