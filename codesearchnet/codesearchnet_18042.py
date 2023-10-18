def check_terminate(self):
        """
        Returns a Bool of whether to terminate.

        Checks whether a satisfactory minimum has been found or whether
        too many iterations have occurred.
        """
        if not self._has_run:
            return False
        else:
            #1-3. errtol, paramtol, model cosine low enough?
            terminate = self.check_completion()

            #4. too many iterations??
            terminate |= (self._num_iter >= self.max_iter)
            return terminate