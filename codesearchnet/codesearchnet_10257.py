def known_publish_date_tags(self, val):
        ''' val must be a dictionary or list of dictionaries
            e.g., {'attrribute': 'name', 'value': 'my-pubdate', 'content': 'datetime'}
                or [{'attrribute': 'name', 'value': 'my-pubdate', 'content': 'datetime'},
                    {'attrribute': 'property', 'value': 'pub_time', 'content': 'content'}]
        '''
        def create_pat_from_dict(val):
            '''Helper function used to create an PublishDatePattern from a dictionary
            '''
            if "tag" in val:
                pat = PublishDatePattern(tag=val["tag"])
                if "attribute" in val:
                    pat.attr = val["attribute"]
                    pat.value = val["value"]
            elif "attribute" in val:
                pat = PublishDatePattern(attr=val["attribute"], value=val["value"],
                                         content=val["content"])
                if "subcontent" in val:
                    pat.subcontent = val["subcontent"]

            if "domain" in val:
                pat.domain = val["domain"]

            return pat

        if isinstance(val, list):
            self._known_publish_date_tags = [
                x if isinstance(x, PublishDatePattern) else create_pat_from_dict(x)
                for x in val
            ] + self.known_publish_date_tags
        elif isinstance(val, PublishDatePattern):
            self._known_publish_date_tags.insert(0, val)
        elif isinstance(val, dict):
            self._known_publish_date_tags.insert(0, create_pat_from_dict(val))
        else:
            raise Exception("Unknown type: {}. Use a PublishDatePattern.".format(type(val)))