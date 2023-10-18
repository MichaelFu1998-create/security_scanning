def save(self, recipe):
        '''
        Saves an AnswerFactory Recipe

        Args:
            recipe (dict): Dictionary specifying a recipe

        Returns:
            AnswerFactory Recipe id
        '''
        # test if this is a create vs. an update
        if 'id' in recipe and recipe['id'] is not None:
            # update -> use put op
            self.logger.debug("Updating existing recipe: " + json.dumps(recipe))
            url = '%(base_url)s/recipe/json/%(recipe_id)s' % {
                'base_url': self.base_url, 'recipe_id': recipe['id']
            }
            r = self.gbdx_connection.put(url, json=recipe)
            try:
                r.raise_for_status()
            except:
                print(r.text)
                raise
            return recipe['id']
        else:
            # create -> use post op
            self.logger.debug("Creating new recipe: " + json.dumps(recipe))
            url = '%(base_url)s/recipe/json' % {
                'base_url': self.base_url
            }
            r = self.gbdx_connection.post(url, json=recipe)
            try:
                r.raise_for_status()
            except:
                print(r.text)
                raise
            recipe_json = r.json()
            return recipe_json['id']