def disassociate_notification_template(self, job_template,
                                           notification_template, status):
        """Disassociate a notification template from this job template.

        =====API DOCS=====
        Disassociate a notification template from this job template.

        :param job_template: The job template to disassociate from.
        :type job_template: str
        :param notification_template: The notification template to be disassociated.
        :type notification_template: str
        :param status: type of notification this notification template should be disassociated from.
        :type status: str
        :returns: Dictionary of only one key "changed", which indicates whether the disassociation succeeded.
        :rtype: dict

        =====API DOCS=====
        """
        return self._disassoc('notification_templates_%s' % status,
                              job_template, notification_template)