def _review_all(self, launchers):
        """
        Runs the review process for all the launchers.
        """
        # Run review of launch args if necessary
        if self.launch_args is not None:
            proceed = self.review_args(self.launch_args,
                                       show_repr=True,
                                       heading='Meta Arguments')
            if not proceed: return False

        reviewers = [self.review_args,
                     self.review_command,
                     self.review_launcher]

        for (count, launcher) in enumerate(launchers):

            # Run reviews for all launchers if desired...
            if not all(reviewer(launcher) for reviewer in reviewers):
                print("\n == Aborting launch ==")
                return False
            # But allow the user to skip these extra reviews
            if len(launchers)!= 1 and count < len(launchers)-1:
                skip_remaining = self.input_options(['Y', 'n','quit'],
                                 '\nSkip remaining reviews?', default='y')

                if skip_remaining == 'y':          break
                elif skip_remaining == 'quit':     return False

        if self.input_options(['y','N'], 'Execute?', default='n') != 'y':
            return False
        else:
            return self._launch_all(launchers)