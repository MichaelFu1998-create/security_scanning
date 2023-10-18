def save(self, project):
        '''
        Saves an AnswerFactory Project

        Args:
            project (dict): Dictionary specifying an AnswerFactory Project.

        Returns:
            AnswerFactory Project id
        '''

        # test if this is a create vs. an update
        if 'id' in project and project['id'] is not None:
            # update -> use put op
            self.logger.debug('Updating existing project: ' + json.dumps(project))
            url = '%(base_url)s/%(project_id)s' % {
                'base_url': self.base_url, 'project_id': project['id']
            }
            r = self.gbdx_connection.put(url, json=project)
            try:
                r.raise_for_status()
            except:
                print(r.text)
                raise
            # updates only get the Accepted response -> return the original project id
            return project['id']
        else:
            self.logger.debug('Creating new project: ' + json.dumps(project))
            # create -> use post op
            url = self.base_url
            r = self.gbdx_connection.post(url, json=project)
            try:
                r.raise_for_status()
            except:
                print(r.text)
                raise
            project_json = r.json()
            # create returns the saved project -> return the project id that's saved
            return project_json['id']