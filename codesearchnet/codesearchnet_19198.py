def artifact(self, counter, stage, job, stage_counter=1):
        """Helper to instantiate an :class:`gocd.api.artifact.Artifact` object

        Args:
          counter (int): The pipeline counter to get the artifact for
          stage: Stage name
          job: Job name
          stage_counter: Defaults to 1

        Returns:
          Artifact: :class:`gocd.api.artifact.Artifact` object
        """
        return Artifact(self.server, self.name, counter, stage, job, stage_counter)