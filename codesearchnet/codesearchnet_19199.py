def console_output(self, instance=None):
        """Yields the output and metadata from all jobs in the pipeline

        Args:
          instance: The result of a :meth:`instance` call, if not supplied
            the latest of the pipeline will be used.

        Yields:
          tuple: (metadata (dict), output (str)).

          metadata contains:
            - pipeline
            - pipeline_counter
            - stage
            - stage_counter
            - job
            - job_result
        """
        if instance is None:
            instance = self.instance()

        for stage in instance['stages']:
            for job in stage['jobs']:
                if job['result'] not in self.final_results:
                    continue

                artifact = self.artifact(
                    instance['counter'],
                    stage['name'],
                    job['name'],
                    stage['counter']
                )
                output = artifact.get('cruise-output/console.log')

                yield (
                    {
                        'pipeline': self.name,
                        'pipeline_counter': instance['counter'],
                        'stage': stage['name'],
                        'stage_counter': stage['counter'],
                        'job': job['name'],
                        'job_result': job['result'],
                    },
                    output.body
                )