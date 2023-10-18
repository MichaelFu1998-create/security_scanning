def wait(self, update_every_seconds=1):
        """
            Wait until the action is marked as completed or with an error.
            It will return True in case of success, otherwise False.

            Optional Args:
                update_every_seconds - int : number of seconds to wait before
                    checking if the action is completed.
        """
        while self.status == u'in-progress':
            sleep(update_every_seconds)
            self.load()

        return self.status == u'completed'