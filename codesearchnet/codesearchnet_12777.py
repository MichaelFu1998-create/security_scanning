def _produce_author_lists(self):
		"""
		Parse authors string to create lists of authors.
		"""

		# post-process author names
		self.authors = self.authors.replace(', and ', ', ')
		self.authors = self.authors.replace(',and ', ', ')
		self.authors = self.authors.replace(' and ', ', ')
		self.authors = self.authors.replace(';', ',')

		# list of authors
		self.authors_list = [author.strip() for author in self.authors.split(',')]

		# simplified representation of author names
		self.authors_list_simple = []

		# author names represented as a tuple of given and family name
		self.authors_list_split = []

		# tests if title already ends with a punctuation mark
		self.title_ends_with_punct = self.title[-1] in ['.', '!', '?'] \
			if len(self.title) > 0 else False

		suffixes = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', "Jr.", "Sr."]
		prefixes = ['Dr.']
		prepositions = ['van', 'von', 'der', 'de', 'den']

		# further post-process author names
		for i, author in enumerate(self.authors_list):
			if author == '':
				continue

			names = author.split(' ')

			# check if last string contains initials
			if (len(names[-1]) <= 3) \
				and names[-1] not in suffixes \
				and all(c in ascii_uppercase for c in names[-1]):
				# turn "Gauss CF" into "C. F. Gauss"
				names = [c + '.' for c in names[-1]] + names[:-1]

			# number of suffixes
			num_suffixes = 0
			for name in names[::-1]:
				if name in suffixes:
					num_suffixes += 1
				else:
					break

			# abbreviate names
			for j, name in enumerate(names[:-1 - num_suffixes]):
				# don't try to abbreviate these
				if j == 0 and name in prefixes:
					continue
				if j > 0 and name in prepositions:
					continue

				if (len(name) > 2) or (len(name) and (name[-1] != '.')):
					k = name.find('-')
					if 0 < k + 1 < len(name):
						# take care of dash
						names[j] = name[0] + '.-' + name[k + 1] + '.'
					else:
						names[j] = name[0] + '.'

			if len(names):
				self.authors_list[i] = ' '.join(names)

				# create simplified/normalized representation of author name
				if len(names) > 1:
					for name in names[0].split('-'):
						name_simple = self.simplify_name(' '.join([name, names[-1]]))
						self.authors_list_simple.append(name_simple)
				else:
					self.authors_list_simple.append(self.simplify_name(names[0]))

				# number of prepositions
				num_prepositions = 0
				for name in names:
					if name in prepositions:
						num_prepositions += 1

				# splitting point
				sp = 1 + num_suffixes + num_prepositions
				self.authors_list_split.append(
					(' '.join(names[:-sp]), ' '.join(names[-sp:])))

		# list of authors in BibTex format
		self.authors_bibtex = ' and '.join(self.authors_list)

		# overwrite authors string
		if len(self.authors_list) > 2:
			self.authors = ', and '.join([
				', '.join(self.authors_list[:-1]),
				self.authors_list[-1]])
		elif len(self.authors_list) > 1:
			self.authors = ' and '.join(self.authors_list)
		else:
			self.authors = self.authors_list[0]