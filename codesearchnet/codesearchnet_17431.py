def verifypartialmatch(self, window_name, object_name, partial_text):
        """
        Verify partial text
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param partial_text: Partial text to match
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        try:
            if re.search(fnmatch.translate(partial_text),
                         self.gettextvalue(window_name,
                                           object_name)):
                return 1
        except:
            pass
        return 0