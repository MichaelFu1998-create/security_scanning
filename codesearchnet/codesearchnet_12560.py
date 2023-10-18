def search(self, lookback_h=12, owner=None, state="all"):
        """Cancels GBDX batch workflow.

         Params:
            lookback_h (int): Look back time in hours.
            owner (str): Workflow owner to search by
            state (str): State to filter by, eg:
                "submitted",
                "scheduled",
                "started",
                "canceled",
                "cancelling",
                "failed",
                "succeeded",
                "timedout",
                "pending",
                "running",
                "complete",
                "waiting",
                "all"

         Returns:
             Batch Workflow status (str).
        """
        postdata = {
            "lookback_h": lookback_h,
            "state": state
        }

        if owner is not None:
            postdata['owner'] = owner

        url = "{}/workflows/search".format(self.base_url)
        headers = {'Content-Type':'application/json'}
        r = self.gbdx_connection.post(url, headers=headers, data=json.dumps(postdata))
        return r.json()