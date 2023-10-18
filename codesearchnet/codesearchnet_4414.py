def construct_end_message(self):
        """Collect the final run information at the time of DFK cleanup.

        Returns:
             - Message dict dumped as json string, ready for UDP
        """
        app_count = self.dfk.task_count

        site_count = len([x for x in self.dfk.config.executors if x.managed])

        app_fails = len([t for t in self.dfk.tasks if
                         self.dfk.tasks[t]['status'] in FINAL_FAILURE_STATES])

        message = {'uuid': self.uuid,
                   'end': time.time(),
                   't_apps': app_count,
                   'sites': site_count,
                   'c_time': None,
                   'failed': app_fails,
                   'test': self.test_mode,
                   }

        return json.dumps(message)