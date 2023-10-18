def find_closed_date_by_commit(self, issue):
        """
        Fill "actual_date" parameter of specified issue by closed date of
        the commit, if it was closed by commit.

        :param dict issue: issue to edit
        """

        if not issue.get('events'):
            return
        # if it's PR -> then find "merged event", in case
        # of usual issue -> find closed date
        compare_string = "merged" if 'merged_at' in issue else "closed"
        # reverse! - to find latest closed event. (event goes in date order)
        # if it were reopened and closed again.
        issue['events'].reverse()
        found_date = False
        for event in issue['events']:
            if event["event"] == compare_string:
                self.set_date_from_event(event, issue)
                found_date = True
                break
        if not found_date:
            # TODO: assert issues, that remain without
            #       'actual_date' hash for some reason.
            print("\nWARNING: Issue without 'actual_date':"
                  " #{0} {1}".format(issue["number"], issue["title"]))