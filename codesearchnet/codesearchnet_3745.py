def update(self, pk=None, create_on_missing=False, monitor=False,
               wait=False, timeout=None, name=None, organization=None):
        """Trigger a project update job within Ansible Tower.
        Only meaningful on non-manual projects.

        =====API DOCS=====
        Update the given project.

        :param pk: Primary key of the project to be updated.
        :type pk: int
        :param monitor: Flag that if set, immediately calls ``monitor`` on the newly launched project update
                        rather than exiting with a success.
        :type monitor: bool
        :param wait: Flag that if set, monitor the status of the project update, but do not print while it is
                     in progress.
        :type wait: bool
        :param timeout: If provided with ``monitor`` flag set, this attempt will time out after the given number
                        of seconds.
        :type timeout: int
        :param name: Name of the project to be updated if ``pk`` is not set.
        :type name: str
        :param organization: Primary key or name of the organization the project to be updated belonging to if
                             ``pk`` is not set.
        :type organization: str
        :returns: Result of subsequent ``monitor`` call if ``monitor`` flag is on; Result of subsequent ``wait``
                  call if ``wait`` flag is on; dictionary of "status" if none of the two flags are on.
        :rtype: dict
        :raises tower_cli.exceptions.CannotStartJob: When the project cannot be updated.

        =====API DOCS=====
        """
        # First, get the appropriate project.
        # This should be uniquely identified at this point, and if not, then
        # we just want the error that `get` will throw to bubble up.
        project = self.get(pk, name=name, organization=organization)
        pk = project['id']

        # Determine whether this project is able to be updated.
        debug.log('Asking whether the project can be updated.',
                  header='details')
        result = client.get('/projects/%d/update/' % pk)
        if not result.json()['can_update']:
            raise exc.CannotStartJob('Cannot update project.')

        # Okay, this project can be updated, according to Tower.
        # Commence the update.
        debug.log('Updating the project.', header='details')
        result = client.post('/projects/%d/update/' % pk)

        project_update_id = result.json()['project_update']

        # If we were told to monitor the project update's status, do so.
        if monitor:
            return self.monitor(project_update_id, parent_pk=pk,
                                timeout=timeout)
        elif wait:
            return self.wait(project_update_id, parent_pk=pk, timeout=timeout)

        # Return the project update ID.
        return {
            'id': project_update_id,
            'changed': True,
        }