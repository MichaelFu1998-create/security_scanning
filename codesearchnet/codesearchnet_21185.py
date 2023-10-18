def random(self, cascadeFetch=False):
		'''
			Random - Returns a random record in current filterset.


			@param cascadeFetch <bool> Default False, If True, all Foreign objects associated with this model
			   will be fetched immediately. If False, foreign objects will be fetched on-access.

			@return - Instance of Model object, or None if no items math current filters
		'''
		matchedKeys = list(self.getPrimaryKeys())
		obj = None
		# Loop so we don't return None when there are items, if item is deleted between getting key and getting obj
		while matchedKeys and not obj:
			key = matchedKeys.pop(random.randint(0, len(matchedKeys)-1))
			obj = self.get(key, cascadeFetch=cascadeFetch)

		return obj