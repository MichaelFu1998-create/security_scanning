def noformat(self):
        """ Temporarily do not use any formatter so that text printed is raw """
        try:
            formats = {}
            for h in self.get_handlers():
                formats[h] = h.formatter
            self.set_formatter(formatter='quiet')
            yield
        except Exception as e:
            raise
        finally:
            for k,v in iteritems(formats):
                k.formatter = v