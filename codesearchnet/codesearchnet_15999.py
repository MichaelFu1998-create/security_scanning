def sound_touch(self, call_params):
        """REST Add soundtouch audio effects to a Call
        """
        path = '/' + self.api_version + '/SoundTouch/'
        method = 'POST'
        return self.request(path, method, call_params)