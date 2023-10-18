def associate_notification_template(self, job_template,
                                        notification_template, status):
        """Associate a notification template from this job template.

        =====API DOCS=====
        Associate a notification template from this job template.

        :param job_template: The job template to associate to.
        :type job_template: str
        :param notification_template: The notification template to be associated.
        :type notification_template: str
        :param status: type of notification this notification template should be associated to.
        :type status: str
        :returns: Dictionary of only one key "changed", which indicates whether the association succeeded.
        :rtype: dict

        =====API DOCS=====
        """
        return self._assoc('notification_templates_%s' % status,
                           job_template, notification_template)