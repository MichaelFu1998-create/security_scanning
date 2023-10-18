def label_suspicious(self, reason):
        """Add suspicion reason and set the suspicious flag."""
        self.suspicion_reasons.append(reason)
        self.is_suspect = True