def start_scan(self, scan_id):
        """
            Starts the scan identified by the scan_id.s
        """
        requests.post(self.url + 'scans/{}/launch'.format(scan_id), verify=False, headers=self.headers)