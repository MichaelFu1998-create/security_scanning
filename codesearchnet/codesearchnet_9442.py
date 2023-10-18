def relative_datetime(self):
        """Return human-readable relative time string."""
        now = datetime.now(timezone.utc)
        tense = "from now" if self.created_at > now else "ago"
        return "{0} {1}".format(humanize.naturaldelta(now - self.created_at), tense)