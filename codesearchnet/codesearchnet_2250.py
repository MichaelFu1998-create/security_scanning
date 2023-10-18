def demo_update(self):
        """
        Performs a demonstration update by calling the demo optimization operation.
        Note that the batch data does not have to be fetched from the demo memory as this is now part of
        the TensorFlow operation of the demo update.
        """
        fetches = self.demo_optimization_output

        self.monitored_session.run(fetches=fetches)