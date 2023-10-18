def pipelines(self):
        """Returns a set of all pipelines from the last response

        Returns:
          set: Response success: all the pipelines available in the response
               Response failure: an empty set
        """
        if not self.response:
            return set()
        elif self._pipelines is None and self.response:
            self._pipelines = set()
            for group in self.response.payload:
                for pipeline in group['pipelines']:
                    self._pipelines.add(pipeline['name'])

        return self._pipelines