def survey(self, pk=None, **kwargs):
        """Get the survey_spec for the job template.
        To write a survey, use the modify command with the --survey-spec parameter.

        =====API DOCS=====
        Get the survey specification of a resource object.

        :param pk: Primary key of the resource to retrieve survey from. Tower CLI will only attempt to
                   read *that* object if ``pk`` is provided (not ``None``).
        :type pk: int
        :param `**kwargs`: Keyword arguments used to look up resource object to retrieve survey if ``pk``
                           is not provided.
        :returns: loaded JSON of the retrieved survey specification of the resource object.
        :rtype: dict
        =====API DOCS=====
        """
        job_template = self.get(pk=pk, **kwargs)
        if settings.format == 'human':
            settings.format = 'json'
        return client.get(self._survey_endpoint(job_template['id'])).json()