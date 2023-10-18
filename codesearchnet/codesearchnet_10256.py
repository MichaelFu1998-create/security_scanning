def known_context_patterns(self, val):
        ''' val must be an ArticleContextPattern, a dictionary, or list of \
            dictionaries
            e.g., {'attr': 'class', 'value': 'my-article-class'}
                or [{'attr': 'class', 'value': 'my-article-class'},
                    {'attr': 'id', 'value': 'my-article-id'}]
        '''
        def create_pat_from_dict(val):
            '''Helper function used to create an ArticleContextPattern from a dictionary
            '''
            if "tag" in val:
                pat = ArticleContextPattern(tag=val["tag"])
                if "attr" in val:
                    pat.attr = val["attr"]
                    pat.value = val["value"]
            elif "attr" in val:
                pat = ArticleContextPattern(attr=val["attr"], value=val["value"])

            if "domain" in val:
                pat.domain = val["domain"]

            return pat

        if isinstance(val, list):
            self._known_context_patterns = [
                x if isinstance(x, ArticleContextPattern) else create_pat_from_dict(x)
                for x in val
            ] + self.known_context_patterns
        elif isinstance(val, ArticleContextPattern):
            self._known_context_patterns.insert(0, val)
        elif isinstance(val, dict):
            self._known_context_patterns.insert(0, create_pat_from_dict(val))
        else:
            raise Exception("Unknown type: {}. Use a ArticleContextPattern.".format(type(val)))