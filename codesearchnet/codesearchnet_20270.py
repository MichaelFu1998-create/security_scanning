def _init_empty(self):
        """Creates the base set of attributes invoice has/needs"""
        self._jsondata = {
            "code": None,
            "currency": "EUR",
            "subject": "",
            "due_date": (datetime.datetime.now().date() + datetime.timedelta(days=14)).isoformat(),
            "issue_date": datetime.datetime.now().date().isoformat(),
            "number": None,
            "type": "outbound",
            "receiver": {
                "name": "",
                "email": "",
                "street": "",
                "city": "",
                "postcode": "",
                "country": ""
            },
            "items": [],
        }