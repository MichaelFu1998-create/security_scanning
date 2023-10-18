def get_is_sim_running(self):
        """Check if the current simulation is running."""
        sim_info = self.simulation_info()
        try:
            progress_info = sim_info['simulation_info_progress']
            ret = progress_info['simulation_progress_is_running']
        except KeyError:  # Simulation has not been created.
            ret = False
        return ret