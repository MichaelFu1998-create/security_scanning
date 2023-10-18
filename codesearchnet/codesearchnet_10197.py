def submit_design_run(self, data_view_id, num_candidates, effort, target=None, constraints=[], sampler="Default"):
        """
        Submits a new experimental design run.

        :param data_view_id: The ID number of the data view to which the
            run belongs, as a string
        :type data_view_id: str
        :param num_candidates: The number of candidates to return
        :type num_candidates: int
        :param target: An :class:``Target`` instance representing
            the design run optimization target
        :type target: :class:``Target``
        :param constraints: An array of design constraints (instances of
            objects which extend :class:``BaseConstraint``)
        :type constraints: list of :class:``BaseConstraint``
        :param sampler: The name of the sampler to use during the design run:
            either "Default" or "This view"
        :type sampler: str
        :return: A :class:`DesignRun` instance containing the UID of the
            new run
        """
        if effort > 30:
            raise CitrinationClientError("Parameter effort must be less than 30 to trigger a design run")

        if target is not None:
            target = target.to_dict()

        constraint_dicts = [c.to_dict() for c in constraints]

        body = {
            "num_candidates": num_candidates,
            "target": target,
            "effort": effort,
            "constraints": constraint_dicts,
            "sampler": sampler
        }

        url = routes.submit_data_view_design(data_view_id)

        response = self._post_json(url, body).json()

        return DesignRun(response["data"]["design_run"]["uid"])