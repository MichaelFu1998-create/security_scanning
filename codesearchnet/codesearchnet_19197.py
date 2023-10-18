def schedule(self, variables=None, secure_variables=None, materials=None,
                 return_new_instance=False, backoff_time=1.0):
        """Schedule a pipeline run

        Aliased as :meth:`run`, :meth:`schedule`, and :meth:`trigger`.

        Args:
          variables (dict, optional): Variables to set/override
          secure_variables (dict, optional): Secure variables to set/override
          materials (dict, optional): Material revisions to be used for
            this pipeline run. The exact format for this is a bit iffy,
            have a look at the official
            `Go pipeline scheduling documentation`__ or inspect a call
            from triggering manually in the UI.
          return_new_instance (bool): Returns a :meth:`history` compatible
            response for the newly scheduled instance. This is primarily so
            users easily can get the new instance number. **Note:** This is done
            in a very naive way, it just checks that the instance number is
            higher than before the pipeline was triggered.
          backoff_time (float): How long between each check for
            :arg:`return_new_instance`.

         .. __: http://api.go.cd/current/#scheduling-pipelines

        Returns:
          Response: :class:`gocd.api.response.Response` object
        """
        scheduling_args = dict(
            variables=variables,
            secure_variables=secure_variables,
            material_fingerprint=materials,
            headers={"Confirm": True},
        )

        scheduling_args = dict((k, v) for k, v in scheduling_args.items() if v is not None)

        # TODO: Replace this with whatever is the official way as soon as gocd#990 is fixed.
        # https://github.com/gocd/gocd/issues/990
        if return_new_instance:
            pipelines = self.history()['pipelines']
            if len(pipelines) == 0:
                last_run = None
            else:
                last_run = pipelines[0]['counter']
            response = self._post('/schedule', ok_status=202, **scheduling_args)
            if not response:
                return response

            max_tries = 10
            while max_tries > 0:
                current = self.instance()
                if not last_run and current:
                    return current
                elif last_run and current['counter'] > last_run:
                    return current
                else:
                    time.sleep(backoff_time)
                    max_tries -= 1

            # I can't come up with a scenario in testing where this would happen, but it seems
            # better than returning None.
            return response
        else:
            return self._post('/schedule', ok_status=202, **scheduling_args)