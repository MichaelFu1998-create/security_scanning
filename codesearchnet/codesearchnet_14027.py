def flush(self, frame):
        '''
        Passes the drawqueue to the sink for rendering
        '''
        self.sink.render(self.size_or_default(), frame, self._drawqueue)
        self.reset_drawqueue()