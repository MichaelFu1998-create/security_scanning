def satisfied_by_checked(self, req):
        """
        Check if requirement is already satisfied by what was previously checked

        :param Requirement req: Requirement to check
        """
        req_man = RequirementsManager([req])

        return any(req_man.check(*checked) for checked in self.checked)