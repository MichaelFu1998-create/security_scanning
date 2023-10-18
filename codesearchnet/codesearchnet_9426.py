def build_default_map(self):
        """Maps config options to the default values used by click, returns :class:`dict`."""
        default_map = {
            "following": {
                "check": self.check_following,
                "timeout": self.timeout,
                "porcelain": self.porcelain,
            },
            "tweet": {
                "twtfile": self.twtfile,
            },
            "timeline": {
                "pager": self.use_pager,
                "cache": self.use_cache,
                "limit": self.limit_timeline,
                "timeout": self.timeout,
                "sorting": self.sorting,
                "porcelain": self.porcelain,
                "twtfile": self.twtfile,
                "update_interval": self.timeline_update_interval,
            },
            "view": {
                "pager": self.use_pager,
                "cache": self.use_cache,
                "limit": self.limit_timeline,
                "timeout": self.timeout,
                "sorting": self.sorting,
                "porcelain": self.porcelain,
                "update_interval": self.timeline_update_interval,
            }
        }
        return default_map