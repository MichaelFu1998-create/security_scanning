def get_object(self, name, description):
        """
        Get object for the statement.
        """
        return Activity(
            id=X_API_ACTIVITY_COURSE,
            definition=ActivityDefinition(
                name=LanguageMap({'en-US': (name or '').encode("ascii", "ignore").decode('ascii')}),
                description=LanguageMap({'en-US': (description or '').encode("ascii", "ignore").decode('ascii')}),
            ),
        )