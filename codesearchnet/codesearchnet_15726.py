def join(self):
        """ master only """
        try:
            self.pipe.put('Q')
            self.thread.join()
        except:
            pass
        finally:
            self.thread = None