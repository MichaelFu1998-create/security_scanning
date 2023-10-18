def get_project_slug(self, bet):
        '''Return slug of a project that given bet is associated with
        or None if bet is not associated with any project.
        '''
        if bet.get('form_params'):
            params = json.loads(bet['form_params'])
            return params.get('project')
        return None