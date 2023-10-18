def wait_for_page_to_load(self):
        """Wait for the page to load."""
        self.wait.until(lambda _: self.loaded)
        self.pm.hook.pypom_after_wait_for_page_to_load(page=self)
        return self