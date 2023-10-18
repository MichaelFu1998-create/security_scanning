def proposal(self, proposer=None, proposal_expiration=None, proposal_review=None):
        """ Return the default proposal buffer

            ... note:: If any parameter is set, the default proposal
               parameters will be changed!
        """
        if not self._propbuffer:
            return self.new_proposal(
                self.tx(), proposer, proposal_expiration, proposal_review
            )
        if proposer:
            self._propbuffer[0].set_proposer(proposer)
        if proposal_expiration:
            self._propbuffer[0].set_expiration(proposal_expiration)
        if proposal_review:
            self._propbuffer[0].set_review(proposal_review)
        return self._propbuffer[0]