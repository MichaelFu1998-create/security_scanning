def vagrant(self, name=''):
        """
        Run the following tasks on a vagrant box.

        First, you need to import this task in your ``fabfile.py``::

            from fabric.api import *
            from burlap.vagrant import vagrant

            @task
            def some_task():
                run('echo hello')

        Then you can easily run tasks on your current Vagrant box::

            $ fab vagrant some_task

        """
        r = self.local_renderer
        config = self.ssh_config(name)

        extra_args = self._settings_dict(config)
        r.genv.update(extra_args)