def mods_genre(self):
		"""
		Guesses an appropriate MODS XML genre type.
		"""

		type2genre = {
				'conference': 'conference publication',
				'book chapter': 'bibliography',
				'unpublished': 'article'
			}
		tp = str(self.type).lower()
		return type2genre.get(tp, tp)