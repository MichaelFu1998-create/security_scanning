def send_zip(self, exercise, file, params):
        """
        Send zipfile to TMC for given exercise
        """

        resp = self.post(
            exercise.return_url,
            params=params,
            files={
                "submission[file]": ('submission.zip', file)
            },
            data={
                "commit": "Submit"
            }
        )
        return self._to_json(resp)