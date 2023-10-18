def remove_all_properties(self, recursive):
        """Remove all associated dead properties."""
        if self.provider.prop_manager:
            self.provider.prop_manager.remove_properties(
                self.get_ref_url(), self.environ
            )