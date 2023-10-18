def wait_for_simulation_stop(self, timeout=None):
        """Block until the simulation is done or timeout seconds exceeded.

        If the simulation stops before timeout, siminfo is returned.
        """
        start = datetime.now()
        while self.get_is_sim_running():
            sleep(0.5)
            if timeout is not None:
                if (datetime.now() - start).seconds >= timeout:
                    ret = None
                    break
        else:
            ret = self.simulation_info()
        return ret