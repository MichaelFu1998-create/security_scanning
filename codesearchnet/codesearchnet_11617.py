def origin(self):
        ''' Read the .yotta_origin.json file (if present), and return the value
            of the 'url' property '''
        if self.origin_info is None:
            self.origin_info = {}
            try:
                self.origin_info = ordered_json.load(os.path.join(self.path, Origin_Info_Fname))
            except IOError:
                pass
        return self.origin_info.get('url', None)