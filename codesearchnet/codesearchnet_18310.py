def stream(self, report):
        """Stream reports to application logs"""

        payload = {
            "agent": {
                "host": report['instance']['hostname'],
                "version": "1.0.0"
            },
            "components": [
                {
                    "name": self.name,
                    "guid": "com.darwinmonroy.aiometrics",
                    "duration": 60,
                    "metrics": {
                        'Component/{}'.format(key): {
                            "total": metric['count'] * metric['avg'],
                            "count": metric['count'],
                            "min": metric['min'],
                            "max": metric['max'],
                            "sum_of_squares": metric['min']**2 + metric['max']**2,
                        } for key, metric in report['traces'].items()
                    }
                }
            ]
        }

        with self.ClientSession() as session:

            try:
                r = yield from session.post(
                    'https://platform-api.newrelic.com/platform/v1/metrics',
                    data=json.dumps(payload),
                    headers=(
                        ('X-License-Key', self.license_key),
                        ('Content-Type', 'application/json'),
                        ('Accept', 'application/json'),
                    )
                )
                r.close()
            except Exception as e:
                # Any exception should affect the execution of the main
                # program, so we must explicitly silence any error caused by
                # by the streaming of metrics
                # TODO: consider the implementation of a retry logic
                logger.exception(e)