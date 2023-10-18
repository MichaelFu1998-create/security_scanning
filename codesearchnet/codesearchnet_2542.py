def load_configs(self):
    """load config files"""
    self.statemgr_config.set_state_locations(self.configs[STATEMGRS_KEY])
    if EXTRA_LINKS_KEY in self.configs:
      for extra_link in self.configs[EXTRA_LINKS_KEY]:
        self.extra_links.append(self.validate_extra_link(extra_link))