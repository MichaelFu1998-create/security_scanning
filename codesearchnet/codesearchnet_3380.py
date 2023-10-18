def get_profiling_stats(self):
        """
        Returns a pstat.Stats instance with profiling results if `run` was called with `should_profile=True`.
        Otherwise, returns `None`.
        """
        profile_file_path = os.path.join(self.workspace, 'profiling.bin')
        try:
            return pstats.Stats(profile_file_path)
        except Exception as e:
            logger.debug(f'Failed to get profiling stats: {e}')
            return None