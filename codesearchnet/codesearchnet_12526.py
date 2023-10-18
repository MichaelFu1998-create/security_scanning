def delete(self, project_id):
        '''
        Deletes a project by id

        Args:
             project_id: The project id to delete

        Returns:
             Nothing
        '''
        self.logger.debug('Deleting project by id: ' + project_id)
        url = '%(base_url)s/%(project_id)s' % {
            'base_url': self.base_url, 'project_id': project_id
        }
        r = self.gbdx_connection.delete(url)
        r.raise_for_status()