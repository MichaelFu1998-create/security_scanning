def invite_by_emails(self, emails):
        """Invite users to a group by emails.

        :param list emails: Emails of users that shall be invited.
        :returns list: Newly created Memberships or Nones.
        """
        assert emails is None or isinstance(emails, list)

        results = []

        for email in emails:
            try:
                user = User.query.filter_by(email=email).one()
                results.append(self.invite(user))
            except NoResultFound:
                results.append(None)

        return results