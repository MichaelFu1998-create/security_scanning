def create_scan(self, host_ips):
        """
            Creates a scan with the given host ips
            Returns the scan id of the created object.
        """
        now = datetime.datetime.now()
        data = {
            "uuid": self.get_template_uuid(),
            "settings": {
                "name": "jackal-" + now.strftime("%Y-%m-%d %H:%M"),
                "text_targets": host_ips
            }
        }
        response = requests.post(self.url + 'scans', data=json.dumps(data), verify=False, headers=self.headers)
        if response:
            result = json.loads(response.text)
            return result['scan']['id']