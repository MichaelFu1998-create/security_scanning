def PlugIn(self):
        """Take next available controller id and plug in to Virtual USB Bus"""
        ids = self.available_ids()
        if len(ids) == 0:
            raise MaxInputsReachedError('Max Inputs Reached')

        self.id = ids[0]

        _xinput.PlugIn(self.id)
        while self.id in self.available_ids():
            pass