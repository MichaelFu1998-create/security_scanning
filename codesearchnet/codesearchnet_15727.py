def slaveraise(self, type, error, traceback):
        """ slave only """
        message = 'E' * 1 + pickle.dumps((type,
            ''.join(tb.format_exception(type, error, traceback))))
        if self.pipe is not None:
            self.pipe.put(message)