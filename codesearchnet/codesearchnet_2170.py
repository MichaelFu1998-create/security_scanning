def close(self):
        """
        Saves the model (of saver dir is given) and closes the session.
        """
        if self.flush_summarizer is not None:
            self.monitored_session.run(fetches=self.flush_summarizer)
        if self.saver_directory is not None:
            self.save(append_timestep=True)
        self.monitored_session.__exit__(None, None, None)