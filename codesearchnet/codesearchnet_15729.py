def abort(self):
        """ ensure the master exit from Barrier """
        self.mutex.release()
        self.turnstile.release()
        self.mutex.release()
        self.turnstile2.release()