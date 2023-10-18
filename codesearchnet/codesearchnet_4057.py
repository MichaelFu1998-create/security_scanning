def wait_for_region_to_load(self):
        """Wait for the page region to load."""
        self.wait.until(lambda _: self.loaded)
        self.pm.hook.pypom_after_wait_for_region_to_load(region=self)
        return self