def _start(self, my_task, force=False):
        """Returns False when successfully fired, True otherwise"""
        if (not hasattr(my_task, 'subprocess')) or my_task.subprocess is None:
            my_task.subprocess = subprocess.Popen(self.args,
                                                  stderr=subprocess.STDOUT,
                                                  stdout=subprocess.PIPE)

        if my_task.subprocess:
            my_task.subprocess.poll()
            if my_task.subprocess.returncode is None:
                # Still waiting
                return False
            else:
                results = my_task.subprocess.communicate()
                my_task.results = results
                return True
        return False