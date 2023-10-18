def get(self, recipe_id):
        '''
        Retrieves an AnswerFactory Recipe by id

        Args:
            recipe_id The id of the recipe

        Returns:
            A JSON representation of the recipe
        '''
        self.logger.debug('Retrieving recipe by id: ' + recipe_id)
        url = '%(base_url)s/recipe/%(recipe_id)s' % {
            'base_url': self.base_url, 'recipe_id': recipe_id
        }
        r = self.gbdx_connection.get(url)
        r.raise_for_status()
        return r.json()