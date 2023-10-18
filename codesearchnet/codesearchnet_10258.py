def known_author_patterns(self, val):
        ''' val must be a dictionary or list of dictionaries
            e.g., {'attrribute': 'name', 'value': 'my-pubdate', 'content': 'datetime'}
                or [{'attrribute': 'name', 'value': 'my-pubdate', 'content': 'datetime'},
                    {'attrribute': 'property', 'value': 'pub_time', 'content': 'content'}]
        '''

        def create_pat_from_dict(val):
            '''Helper function used to create an AuthorPatterns from a dictionary
            '''
            if "tag" in val:
                pat = AuthorPattern(tag=val["tag"])
                if "attribute" in val:
                    pat.attr = val["attribute"]
                    pat.value = val["value"]
            elif "attribute" in val:
                pat = AuthorPattern(attr=val["attribute"], value=val["value"],
                                    content=val["content"])
            if "subpattern" in val:
                pat.subpattern = create_pat_from_dict(val["subpattern"])

            return pat

        if isinstance(val, list):
            self._known_author_patterns = [
                x if isinstance(x, AuthorPattern) else create_pat_from_dict(x)
                for x in val
            ] + self.known_author_patterns
        elif isinstance(val, AuthorPattern):
            self._known_author_patterns.insert(0, val)
        elif isinstance(val, dict):
            self._known_author_patterns.insert(0, create_pat_from_dict(val))
        else:
            raise Exception("Unknown type: {}. Use an AuthorPattern.".format(type(val)))