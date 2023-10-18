def wait_for_environments(self, environment_names, health=None, status=None, version_label=None,
                              include_deleted=True, use_events=True):
        """
        Waits for an environment to have the given version_label
        and to be in the green state
        """

        # turn into a list
        if not isinstance(environment_names, (list, tuple)):
            environment_names = [environment_names]
        environment_names = environment_names[:]

        # print some stuff
        s = "Waiting for environment(s) " + (", ".join(environment_names)) + " to"
        if health is not None:
            s += " have health " + health
        else:
            s += " have any health"
        if version_label is not None:
            s += " and have version " + version_label
        if status is not None:
            s += " and have status " + status
        out(s)

        started = time()
        seen_events = list()

        for env_name in environment_names:
            (events, next_token) = self.describe_events(env_name, start_time=datetime.now().isoformat())
            for event in events:
                seen_events.append(event)

        while True:
            # bail if they're all good
            if len(environment_names) == 0:
                break

            # wait
            sleep(10)

            # # get the env
            environments = self.ebs.describe_environments(
                application_name=self.app_name,
                environment_names=environment_names,
                include_deleted=include_deleted)

            environments = environments['DescribeEnvironmentsResponse']['DescribeEnvironmentsResult']['Environments']
            if len(environments) <= 0:
                raise Exception("Couldn't find any environments")

            # loop through and wait
            for env in environments[:]:
                env_name = env['EnvironmentName']

                # the message
                msg = "Environment " + env_name + " is " + str(env['Health'])
                if version_label is not None:
                    msg = msg + " and has version " + str(env['VersionLabel'])
                if status is not None:
                    msg = msg + " and has status " + str(env['Status'])

                # what we're doing
                good_to_go = True
                if health is not None:
                    good_to_go = good_to_go and str(env['Health']) == health
                if status is not None:
                    good_to_go = good_to_go and str(env['Status']) == status
                if version_label is not None:
                    good_to_go = good_to_go and str(env['VersionLabel']) == version_label

                # allow a certain number of Red samples before failing
                if env['Status'] == 'Ready' and env['Health'] == 'Red':
                    if 'RedCount' not in env:
                        env['RedCount'] = 0

                    env['RedCount'] += 1
                    if env['RedCount'] > MAX_RED_SAMPLES:
                        out('Deploy failed')
                        raise Exception('Ready and red')

                # log it
                if good_to_go:
                    out(msg + " ... done")
                    environment_names.remove(env_name)
                else:
                    out(msg + " ... waiting")

                # log events
                (events, next_token) = self.describe_events(env_name, start_time=datetime.now().isoformat())
                for event in events:
                    if event not in seen_events:
                        out("["+event['Severity']+"] "+event['Message'])
                        seen_events.append(event)

            # check the time
            elapsed = time() - started
            if elapsed > self.wait_time_secs:
                message = "Wait time for environment(s) {environments} to be {health} expired".format(
                    environments=" and ".join(environment_names), health=(health or "Green")
                )
                raise Exception(message)