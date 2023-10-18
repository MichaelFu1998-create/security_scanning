def _validate_status(self):
        """Validates Status information. Raises errors for required
        properties."""
        if not self.id:
            msg = "No 'id' in Status for request '{}'"
            raise ValidationError(msg.format(self.url))

        if not self.status:
            msg = "No 'status' in Status for request '{}'"
            raise ValidationError(msg.format(self.url))

        if self.total_count is None:
            msg = "No 'total_count' in Status for request '{}'"
            raise ValidationError(msg.format(self.url))

        if self.success_count is None:
            msg = "No 'success_count' in Status for request '{}'"
            raise ValidationError(msg.format(self.url))

        if self.failure_count is None:
            msg = "No 'failure_count' in Status for request '{}'"
            raise ValidationError(msg.format(self.url))

        if self.pending_count is None:
            msg = "No 'pending_count' in Status for request '{}'"
            raise ValidationError(msg.format(self.url))

        if len(self.successes) != self.success_count:
            msg = "Found successes={}, but success_count={} in status '{}'"
            raise ValidationError(msg.format(self.successes,
                                             self.success_count,
                                             self.id))

        if len(self.pendings) != self.pending_count:
            msg = "Found pendings={}, but pending_count={} in status '{}'"
            raise ValidationError(msg.format(self.pendings,
                                             self.pending_count,
                                             self.id))

        if len(self.failures) != self.failure_count:
            msg = "Found failures={}, but failure_count={} in status '{}'"
            raise ValidationError(msg.format(self.failures,
                                             self.failure_count,
                                             self.id))

        if (self.success_count + self.pending_count + self.failure_count !=
                self.total_count):
            msg = ("(success_count={} + pending_count={} + "
                   "failure_count={}) != total_count={} in status '{}'")
            raise ValidationError(msg.format(self.success_count,
                                             self.pending_count,
                                             self.failure_count,
                                             self.total_count,
                                             self.id))