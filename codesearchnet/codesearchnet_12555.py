def get_stdout(self, workflow_id, task_id):
        """Get stdout for a particular task.

         Args:
             workflow_id (str): Workflow id.
             task_id (str): Task id.

         Returns:
             Stdout of the task (string).
        """
        url = '%(wf_url)s/%(wf_id)s/tasks/%(task_id)s/stdout' % {
            'wf_url': self.workflows_url, 'wf_id': workflow_id, 'task_id': task_id
        }
        r = self.gbdx_connection.get(url)
        r.raise_for_status()

        return r.text