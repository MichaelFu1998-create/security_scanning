def __base_state(self, containers):
        '''
        Convert blockade ID and container information into
        a state dictionary object.
        '''
        return dict(blockade_id=self._blockade_id,
                    containers=containers,
                    version=self._state_version)