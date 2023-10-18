def get_short_version(self):
        '''obtain the shory geoserver version
        '''
        gs_version = self.get_version()
        match = re.compile(r'[^\d.]+')
        return match.sub('', gs_version).strip('.')