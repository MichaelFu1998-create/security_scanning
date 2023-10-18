def train_and_validate_to_end(self, validate_step_size=50):
        """A helper function that shows how to train and validate a model at the same time.

        Parameters
        ----------
        validate_step_size : int
            Validate the training network every N steps.

        """
        while not self._sess.should_stop():
            self.train_on_batch()  # Run a training step synchronously.
            if self.global_step % validate_step_size == 0:
                # logging.info("Average loss for validation dataset: %s" % self.get_validation_metrics())
                log_str = 'step: %d, ' % self.global_step
                for n, m in self.validation_metrics:
                    log_str += '%s: %f, ' % (n.name, m)
                logging.info(log_str)