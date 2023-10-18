def get(self):
    """ get method """
    clusters = [statemgr.name for statemgr in self.tracker.state_managers]

    self.write_success_response(clusters)