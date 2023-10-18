def get_template_uuid(self):
        """
            Retrieves the uuid of the given template name.
        """
        response = requests.get(self.url + 'editor/scan/templates', headers=self.headers, verify=False)
        templates = json.loads(response.text)
        for template in templates['templates']:
            if template['name'] == self.template_name:
                return template['uuid']