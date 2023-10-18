def get_params(self, url):
        """
        Extract the named parameters from a url regex.  If the url regex does not contain
        named parameters, they will be keyed _0, _1, ...
        
        * Named parameters
        Regex:
        /photos/^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<object_id>\d+)/
        
        URL:
        http://www2.ljworld.com/photos/2009/oct/11/12345/
        
        Return Value:
        {u'day': '11', u'month': 'oct', u'object_id': '12345', u'year': '2009'}
        
        * Unnamed parameters
        Regex:
        /blah/([\w-]+)/(\d+)/
        
        URL:
        http://www.example.com/blah/hello/123/
        
        Return Value:
        {u'_0': 'hello', u'_1': '123'}
        """
        match = re.match(self.regex, url)
        if match is not None:
            params = match.groupdict()
            if not params:
                params = {}
                for i, group in enumerate(match.groups()[1:]):
                    params['_%s' % i] = group
            return params
        
        raise OEmbedException('No regex matched the url %s' % (url))