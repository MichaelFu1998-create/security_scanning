def stage(self, pipeline_name, stage_name, pipeline_counter=None):
        """Returns an instance of :class:`Stage`

        Args:
            pipeline_name (str): Name of the pipeline the stage belongs to
            stage_name (str): Name of the stage to act on
            pipeline_counter (int): The pipeline instance the stage is for.

        Returns:
          Stage: an instantiated :class:`Stage`.
        """
        return Stage(self, pipeline_name, stage_name, pipeline_counter=pipeline_counter)