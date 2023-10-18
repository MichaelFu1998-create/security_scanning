def sound_touch_stop(self, call_params):
        """REST Remove soundtouch audio effects on a Call
        """
        path = '/' + self.api_version + '/SoundTouchStop/'
        method = 'POST'
        return self.request(path, method, call_params)